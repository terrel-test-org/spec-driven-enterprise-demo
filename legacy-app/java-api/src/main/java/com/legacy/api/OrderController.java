package com.legacy.api;

import java.sql.*;
import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * OrderController - REST API endpoints for order management
 * 
 * NOTE: This is legacy code maintained for backwards compatibility.
 * Originally written in 2015, migrated from Struts in 2017.
 * 
 * @deprecated Use new OrderServiceV2 when available (planned Q3 2023)
 */
public class OrderController {
    
    private static final String DB_URL = "jdbc:sqlite:enterprise.db";
    private static final int MAX_RESULTS = 100;
    private static final double HIGH_VALUE_THRESHOLD = 10000.0;
    
    private Connection connection;
    private CustomerService customerService;
    
    public OrderController() {
        this.customerService = new CustomerService();
        initializeConnection();
    }
    
    private void initializeConnection() {
        try {
            connection = DriverManager.getConnection(DB_URL);
        } catch (SQLException e) {
            System.err.println("Failed to connect to database: " + e.getMessage());
        }
    }
    
    /**
     * GET /orders/{id}
     */
    public Map<String, Object> getOrder(int orderId) {
        Map<String, Object> result = new HashMap<>();
        
        try {
            // SQL Injection vulnerability - id is not parameterized
            String sql = "SELECT * FROM orders WHERE id = " + orderId;
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            
            if (rs.next()) {
                result.put("id", rs.getInt("id"));
                result.put("customer_id", rs.getInt("customer_id"));
                result.put("order_date", rs.getString("order_date"));
                result.put("status", rs.getString("status"));
                result.put("total_amount", rs.getDouble("total_amount"));
                result.put("items", getOrderItems(orderId));
                
                // N+1 query pattern
                Map<String, Object> customer = customerService.getCustomer(rs.getInt("customer_id"));
                result.put("customer", customer);
                result.put("success", true);
            } else {
                result.put("success", false);
                result.put("error", "Order not found");
            }
            
            rs.close();
            stmt.close();
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    /**
     * GET /orders - List orders with filters
     */
    public Map<String, Object> listOrders(String status, Integer customerId, int page, int pageSize) {
        Map<String, Object> result = new HashMap<>();
        List<Map<String, Object>> orders = new ArrayList<>();
        
        // SQL Injection vulnerable query building
        StringBuilder sql = new StringBuilder("SELECT * FROM orders WHERE 1=1");
        
        if (status != null && !status.isEmpty()) {
            sql.append(" AND status = '").append(status).append("'");
        }
        if (customerId != null) {
            sql.append(" AND customer_id = ").append(customerId);
        }
        
        sql.append(" ORDER BY created_at DESC");
        sql.append(" LIMIT ").append(Math.min(pageSize, MAX_RESULTS));
        sql.append(" OFFSET ").append(page * pageSize);
        
        try {
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery(sql.toString());
            
            while (rs.next()) {
                Map<String, Object> order = new HashMap<>();
                order.put("id", rs.getInt("id"));
                order.put("customer_id", rs.getInt("customer_id"));
                order.put("status", rs.getString("status"));
                order.put("total_amount", rs.getDouble("total_amount"));
                orders.add(order);
            }
            
            result.put("orders", orders);
            result.put("page", page);
            result.put("count", orders.size());
            result.put("success", true);
            
            rs.close();
            stmt.close();
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    /**
     * POST /orders - Create new order
     */
    public Map<String, Object> createOrder(int customerId, List<Map<String, Object>> items, 
                                           String shippingAddress) {
        Map<String, Object> result = new HashMap<>();
        
        // Validate customer
        Map<String, Object> customer = customerService.getCustomer(customerId);
        if (customer == null || customer.get("error") != null) {
            result.put("success", false);
            result.put("error", "Invalid customer");
            return result;
        }
        
        String accountStatus = (String) customer.get("account_status");
        if ("hold".equals(accountStatus) || "closed".equals(accountStatus)) {
            result.put("success", false);
            result.put("error", "Customer account is not active");
            return result;
        }
        
        // Calculate total
        double total = 0.0;
        for (Map<String, Object> item : items) {
            double price = ((Number) item.get("unit_price")).doubleValue();
            int quantity = ((Number) item.get("quantity")).intValue();
            double discount = item.containsKey("discount") ? 
                ((Number) item.get("discount")).doubleValue() : 0.0;
            total += price * quantity * (1 - discount / 100);
        }
        
        // Check credit limit
        double creditLimit = ((Number) customer.get("credit_limit")).doubleValue();
        if (total > creditLimit) {
            result.put("success", false);
            result.put("error", "Order exceeds credit limit");
            return result;
        }
        
        String status = total > HIGH_VALUE_THRESHOLD ? "pending_approval" : "confirmed";
        
        try {
            String now = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            
            String insertSql = "INSERT INTO orders (customer_id, order_date, status, total_amount, " +
                              "shipping_address, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)";
            
            PreparedStatement pstmt = connection.prepareStatement(insertSql, 
                Statement.RETURN_GENERATED_KEYS);
            pstmt.setInt(1, customerId);
            pstmt.setString(2, now);
            pstmt.setString(3, status);
            pstmt.setDouble(4, total);
            pstmt.setString(5, shippingAddress);
            pstmt.setString(6, now);
            pstmt.setString(7, now);
            
            pstmt.executeUpdate();
            
            ResultSet generatedKeys = pstmt.getGeneratedKeys();
            int orderId = generatedKeys.next() ? generatedKeys.getInt(1) : -1;
            
            for (Map<String, Object> item : items) {
                insertOrderItem(orderId, item);
            }
            
            result.put("success", true);
            result.put("order_id", orderId);
            result.put("status", status);
            result.put("total", total);
            
            pstmt.close();
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    private void insertOrderItem(int orderId, Map<String, Object> item) throws SQLException {
        String sql = "INSERT INTO order_items (order_id, product_id, product_name, " +
                    "quantity, unit_price, total_price, discount_percent) VALUES (?, ?, ?, ?, ?, ?, ?)";
        
        PreparedStatement pstmt = connection.prepareStatement(sql);
        
        int quantity = ((Number) item.get("quantity")).intValue();
        double unitPrice = ((Number) item.get("unit_price")).doubleValue();
        double discount = item.containsKey("discount") ? ((Number) item.get("discount")).doubleValue() : 0.0;
        
        pstmt.setInt(1, orderId);
        pstmt.setInt(2, ((Number) item.get("product_id")).intValue());
        pstmt.setString(3, (String) item.getOrDefault("name", "Unknown Product"));
        pstmt.setInt(4, quantity);
        pstmt.setDouble(5, unitPrice);
        pstmt.setDouble(6, unitPrice * quantity * (1 - discount / 100));
        pstmt.setDouble(7, discount);
        
        pstmt.executeUpdate();
        pstmt.close();
    }
    
    private List<Map<String, Object>> getOrderItems(int orderId) throws SQLException {
        List<Map<String, Object>> items = new ArrayList<>();
        
        PreparedStatement pstmt = connection.prepareStatement(
            "SELECT * FROM order_items WHERE order_id = ?");
        pstmt.setInt(1, orderId);
        ResultSet rs = pstmt.executeQuery();
        
        while (rs.next()) {
            Map<String, Object> item = new HashMap<>();
            item.put("product_id", rs.getInt("product_id"));
            item.put("product_name", rs.getString("product_name"));
            item.put("quantity", rs.getInt("quantity"));
            item.put("unit_price", rs.getDouble("unit_price"));
            items.add(item);
        }
        
        rs.close();
        pstmt.close();
        return items;
    }
    
    /**
     * PUT /orders/{id}/status
     */
    public Map<String, Object> updateOrderStatus(int orderId, String newStatus, String updatedBy) {
        Map<String, Object> result = new HashMap<>();
        
        String[] validStatuses = {"pending", "confirmed", "processing", "shipped", "delivered", "cancelled"};
        boolean isValid = Arrays.asList(validStatuses).contains(newStatus);
        
        if (!isValid) {
            result.put("success", false);
            result.put("error", "Invalid status: " + newStatus);
            return result;
        }
        
        try {
            String now = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            PreparedStatement pstmt = connection.prepareStatement(
                "UPDATE orders SET status = ?, updated_at = ?, processed_by = ? WHERE id = ?");
            pstmt.setString(1, newStatus);
            pstmt.setString(2, now);
            pstmt.setString(3, updatedBy);
            pstmt.setInt(4, orderId);
            
            int rowsAffected = pstmt.executeUpdate();
            pstmt.close();
            
            result.put("success", rowsAffected > 0);
            if (rowsAffected == 0) {
                result.put("error", "Order not found");
            }
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    public void close() {
        try {
            if (connection != null && !connection.isClosed()) {
                connection.close();
            }
        } catch (SQLException e) {
            System.err.println("Error closing connection: " + e.getMessage());
        }
    }
}
