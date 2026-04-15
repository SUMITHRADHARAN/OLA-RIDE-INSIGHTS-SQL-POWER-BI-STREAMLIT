-- Creating Database 
Create Database Ola_Rides;
-- Selecting Database
Use Ola_Rides;

-- ==============================================================================
-- SECTION 1: KEY PERFORMANCE INDICATOR QUERIES (Direct Selects)
-- ==============================================================================

-- 1. Successful Bookings
SELECT * FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Success';

-- 2. Avg ride distance for each vehicle type
SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS avg_ride_distance
FROM Ola_Ride_Cleaned_File
GROUP BY Vehicle_Type;

-- 3. Total cancelled rides by customers
SELECT COUNT(*) AS total_rides FROM Ola_Ride_Cleaned_File 
WHERE Booking_Status = 'Canceled by Customer';

-- 4. Top 5 customers (highest number of rides)
SELECT Customer_ID, COUNT(*) AS total_rides FROM Ola_Ride_Cleaned_File
GROUP BY Customer_ID ORDER BY total_rides DESC LIMIT 5;

-- 5. Rides cancelled by drivers (Personal/Car issues)
SELECT COUNT(*) AS total_rides FROM Ola_Ride_Cleaned_File
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- 6. Max/Min driver ratings (Prime Sedan)
SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating
FROM Ola_Ride_Cleaned_File WHERE Vehicle_Type = 'Prime Sedan';

-- 7. UPI Payments
SELECT * FROM Ola_Ride_Cleaned_File WHERE Payment_Method = 'UPI';

-- 8. Avg customer rating per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS avg_rating
FROM Ola_Ride_Cleaned_File GROUP BY Vehicle_Type;

-- 9. Total booking value (Successful)
SELECT SUM(Booking_Value) AS total_successful_value
FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Success';

-- 10. Incomplete rides with reasons
SELECT * FROM Ola_Ride_Cleaned_File 
WHERE Incomplete_Rides = 'Yes' AND Incomplete_Rides_Reason <> 'Unknown';

-- ==============================================================================
-- SECTION 2: VIEW CREATIONS (Standardized for Ola_Ride_Cleaned_File)
-- ==============================================================================

-- Overall Ride Volume
CREATE OR REPLACE VIEW ride_volume_over_time AS
SELECT DATE(Date) AS ride_date, COUNT(*) AS total_rides
FROM Ola_Ride_Cleaned_File GROUP BY DATE(Date);

-- Booking Status Breakdown
CREATE OR REPLACE VIEW booking_status_breakdown AS
SELECT Booking_Status, COUNT(*) AS total_rides
FROM Ola_Ride_Cleaned_File GROUP BY Booking_Status;

-- Top 5 Vehicle Types by Distance
CREATE OR REPLACE VIEW top5_vehicle_type_by_distance AS
SELECT Vehicle_Type, SUM(Ride_Distance) AS total_distance
FROM Ola_Ride_Cleaned_File GROUP BY Vehicle_Type ORDER BY total_distance DESC;

-- Revenue by Payment Method
CREATE OR REPLACE VIEW revenue_by_payment_method AS
SELECT Payment_Method, SUM(Booking_Value) AS total_revenue
FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Success' GROUP BY Payment_Method;

-- Customer Cancellation Reasons
CREATE OR REPLACE VIEW canceled_rides_customer AS
SELECT Canceled_Rides_by_Customer AS cancel_reason, COUNT(*) AS cancel_count
FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Canceled by Customer' 
AND Canceled_Rides_by_Customer <> 'Unknown' GROUP BY Canceled_Rides_by_Customer;

-- Driver Cancellation Reasons
CREATE OR REPLACE VIEW canceled_rides_driver AS
SELECT Canceled_Rides_by_Driver AS cancel_reason, COUNT(*) AS cancel_count
FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Canceled by Driver' 
AND Canceled_Rides_by_Driver <> 'Unknown' GROUP BY Canceled_Rides_by_Driver;

-- Driver Ratings Summary
CREATE OR REPLACE VIEW driver_ratings_summary AS
SELECT Vehicle_Type, ROUND(AVG(Driver_Ratings), 2) AS avg_driver_ratings, 
MAX(Driver_Ratings) AS max_driver_ratings, MIN(Driver_Ratings) AS min_driver_ratings
FROM Ola_Ride_Cleaned_File GROUP BY Vehicle_Type;

-- Customer Ratings Summary
CREATE OR REPLACE VIEW customer_ratings_summary AS
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS avg_customer_ratings, 
MAX(Customer_Rating) AS max_customer_ratings, MIN(Customer_Rating) AS min_customer_ratings
FROM Ola_Ride_Cleaned_File GROUP BY Vehicle_Type;