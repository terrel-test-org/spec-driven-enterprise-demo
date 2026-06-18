package com.legacy.api;

import java.sql.*;
import java.util.*;

/**
 * CustomerService - Customer data access and business logic
 * 
 * This service handles all customer-related operations.
 * Some methods duplicate logic found in the Python services.
 * 
 * @version 1.2.0
 */
public class CustomerService {
    
    private static final String DB_URL = "jdbc:sqlite:enterprise.db";
    private Connection connection;
    
    public CustomerService() {
        try {
            connection = DriverManager.getConnection(DB_URL);
        } catch (SQLException e) {
            System.err.println("CustomerService: Failed to connect: " + e.getMessage());
        }
    }
    
    /**
     * Get customer by ID
     */
    public Map<String, Object> getCustomer(int customerId) {
        Map<String, Object> result = new HashMap<>();
        
        try {
            PreparedStatement pstmt = connection.prepareStatement(
                "SELECT * FROM customers WHERE id = ?");
            pstmt.setInt(1, customerId);
            ResultSet rs = pstmt.executeQuery();
            
            if (rs.next()) {
                result.put("id", rs.getInt("id"));
                result.put("name", rs.getString("name"));
                result.put("email", rs.getString("email"));
                result.put("phone", rs.getString("phone"));
                result.put("address", rs.getString("address"));
                result.put("credit_limit", rs.getDouble("credit_limit"));
                result.put("account_status", rs.getString("account_status"));
                result.put("created_date", rs.getString("created_date"));
            } else {
                result.put("error", "Customer not found");
            }
            
            rs.close();
            pstmt.close();
        } catch (SQLException e) {
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    /**
     * Create a new customer
     */
    public Map<String, Object> createCustomer(String name, String email, String phone, 
                                               String address, Double creditLimit) {
        Map<String, Object> result = new HashMap<>();
        
        // Check for duplicate email - but no unique constraint in DB!
        try {
            PreparedStatement check = connection.prepareStatement(
                "SELECT id FROM customers WHERE email = ?");
            check.setString(1, email);
            ResultSet rs = check.executeQuery();
            
            if (rs.next()) {
                result.put("success", false);
                result.put("error", "Email already exists");
                return result;
            }
            rs.close();
            check.close();
            
            String sql = "INSERT INTO customers (name, email, phone, address, credit_limit, " +
                        "account_status, created_date) VALUES (?, ?, ?, ?, ?, 'active', datetime('now'))";
            
            PreparedStatement pstmt = connection.prepareStatement(sql, 
                Statement.RETURN_GENERATED_KEYS);
            pstmt.setString(1, name);
            pstmt.setString(2, email);
            pstmt.setString(3, phone);
            pstmt.setString(4, address);
            pstmt.setDouble(5, creditLimit != null ? creditLimit : 5000.0);
            
            pstmt.executeUpdate();
            
            ResultSet keys = pstmt.getGeneratedKeys();
            int customerId = keys.next() ? keys.getInt(1) : -1;
            
            result.put("success", true);
            result.put("customer_id", customerId);
            
            pstmt.close();
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    /**
     * Update customer credit limit
     * Business rule: Cannot exceed $100,000 without VP approval
     */
    public Map<String, Object> updateCreditLimit(int customerId, double newLimit, String approvedBy) {
        Map<String, Object> result = new HashMap<>();
        
        // Hardcoded business rule
        if (newLimit > 100000 && !"VP".equals(approvedBy)) {
            result.put("success", false);
            result.put("error", "Credit limits over $100,000 require VP approval");
            return result;
        }
        
        try {
            PreparedStatement pstmt = connection.prepareStatement(
                "UPDATE customers SET credit_limit = ? WHERE id = ?");
            pstmt.setDouble(1, newLimit);
            pstmt.setInt(2, customerId);
            
            int rows = pstmt.executeUpdate();
            pstmt.close();
            
            result.put("success", rows > 0);
            if (rows == 0) {
                result.put("error", "Customer not found");
            }
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    /**
     * Put customer account on hold
     */
    public Map<String, Object> setAccountStatus(int customerId, String status, String reason) {
        Map<String, Object> result = new HashMap<>();
        
        String[] validStatuses = {"active", "hold", "closed", "suspended"};
        if (!Arrays.asList(validStatuses).contains(status)) {
            result.put("success", false);
            result.put("error", "Invalid status");
            return result;
        }
        
        try {
            PreparedStatement pstmt = connection.prepareStatement(
                "UPDATE customers SET account_status = ? WHERE id = ?");
            pstmt.setString(1, status);
            pstmt.setInt(2, customerId);
            
            int rows = pstmt.executeUpdate();
            pstmt.close();
            
            // Log reason somewhere... (not implemented)
            System.out.println("Account " + customerId + " set to " + status + ": " + reason);
            
            result.put("success", rows > 0);
        } catch (SQLException e) {
            result.put("success", false);
            result.put("error", e.getMessage());
        }
        
        return result;
    }
    
    /**
     * Get customer order history summary
     */
    public Map<String, Object> getCustomerSummary(int customerId) {
        Map<String, Object> summary = new HashMap<>();
        
        try {
            // Basic info
            Map<String, Object> customer = getCustomer(customerId);
            if (customer.containsKey("error")) {
                return customer;
            }
            summary.putAll(customer);
            
            // Order stats - multiple queries, could be optimized
            Statement stmt = connection.createStatement();
            
            ResultSet rs = stmt.executeQuery(
                "SELECT COUNT(*) as total, SUM(total_amount) as revenue " +
                "FROM orders WHERE customer_id = " + customerId);
            if (rs.next()) {
                summary.put("total_orders", rs.getInt("total"));
                summary.put("total_revenue", rs.getDouble("revenue"));
            }
            rs.close();
            
            // Recent order
            rs = stmt.executeQuery(
                "SELECT * FROM orders WHERE customer_id = " + customerId + 
                " ORDER BY created_at DESC LIMIT 1");
            if (rs.next()) {
                Map<String, Object> lastOrder = new HashMap<>();
                lastOrder.put("id", rs.getInt("id"));
                lastOrder.put("date", rs.getString("order_date"));
                lastOrder.put("total", rs.getDouble("total_amount"));
                lastOrder.put("status", rs.getString("status"));
                summary.put("last_order", lastOrder);
            }
            rs.close();
            stmt.close();
            
        } catch (SQLException e) {
            summary.put("error", e.getMessage());
        }
        
        return summary;
    }
}
