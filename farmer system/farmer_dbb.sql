-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `farmers_dbb`
--

-- --------------------------------------------------------

--
-- Table structure for table `addagroproducts`
--

CREATE TABLE IF NOT EXISTS `addagroproducts` (
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pid` int(11) NOT NULL,
  `productname` varchar(100) NOT NULL,
  `productdesc` text NOT NULL,
  `price` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `addagroproducts`
--

INSERT INTO `addagroproducts` (`username`, `email`, `pid`, `productname`, `productdesc`, `price`) VALUES
('test', 'test@gmail.com', 7, 'GIRIJA CAULIFLOWER', ' Tips for Growing Cauliflower. Well drained medium loam and or sandy loam soils are suitable.', 520);
-- --------------------------------------------------------

--
-- Table structure for table `trig`
--

CREATE TABLE IF NOT EXISTS `trig` (
  `id` int(11) NOT NULL,
  `farmer_id` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trig`
--

INSERT INTO `trig` (`id`, `farmer_id`, `action`, `timestamp`) VALUES
(1, '2', 'FARMER UPDATED', '2021-01-19 23:04:44'),
(2, '2', 'FARMER DELETED', '2021-01-19 23:04:58'),
(3, '8', 'Farmer Inserted', '2021-01-19 23:16:52'),
(4, '8', 'FARMER UPDATED', '2021-01-19 23:17:17'),
(5, '8', 'FARMER DELETED', '2021-01-19 23:18:54');


-- --------------------------------------------------------

--
-- Table structure for table `farmers`
--
CREATE TABLE IF NOT EXISTS `farmers` (
    farmer_id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    farming_experience INT NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    state VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL,
    town_village VARCHAR(255) NOT NULL,
    pincode INT NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

insert into `farmers` values (1,'john','smith',DATE '1990-12-10',15,'484494949','Karnataka','Bangalore','kengeri',583113);


--
-- Triggers `farmers`
--
DELIMITER $$
CREATE TRIGGER `deletion` BEFORE DELETE ON `farmers` FOR EACH ROW INSERT INTO trig VALUES(null,OLD.farmer_id,'FARMER DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `insertion` AFTER INSERT ON `farmers` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.farmer_id,'Farmer Inserted',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `updation` AFTER UPDATE ON `farmers` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.farmer_id,'FARMER UPDATED',NOW())
$$
DELIMITER ;







-- Table structure for table `land_details`
CREATE TABLE IF NOT EXISTS `land_details`(
    land_id  INT AUTO_INCREMENT PRIMARY KEY,
    size FLOAT NOT NULL,
    location VARCHAR(255) NOT NULL,
    soil_type VARCHAR(255) NOT NULL,
    irrigation_system VARCHAR(255) NOT NULL,
    farmer_id INT,
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Dumping data for table `land_details`
--

INSERT INTO `land_details` VALUES
(1,2.5,'bangalore','black soil','drip irrigation',1);


CREATE TABLE IF NOT EXISTS `crops` (
    crop_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    planting_date DATE NOT NULL,
    harvest_date DATE NOT NULL,
    expected_yield INT NOT NULL,
    actual_yield INT NOT NULL,
    fertilizers_used VARCHAR(255) NOT NULL,
    land_id INT,
    FOREIGN KEY (land_id) REFERENCES land_details(land_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


insert into `crops` values(1,'maize',DATE '2023-10-20',DATE '2024-03-24',1300,1200,'Nitrogen fertilizer',1);

CREATE TABLE IF NOT EXISTS `farm_equipment` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    purchase_date DATE NOT NULL,
    farmer_id INT,
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;

insert into `farm_equipment` values(1,'tractor','Mahindra',300000.00,DATE '2022-10-01',1);


CREATE TABLE IF NOT EXISTS `farm_animals` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    breed VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    health_status VARCHAR(255) NOT NULL,
    farmer_id INT,
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;

insert into `farm_animals` values(1,'cattle','Krishna valley','male',3,'good',1);


CREATE TABLE IF NOT EXISTS `labour` (
    labour_id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    state VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL,
    town_village VARCHAR(255) NOT NULL,
    pincode  INT NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;

insert into `labour` values(1,'john','smith','male','1738483839','karnataka','bangalore','kengeri',560060);


CREATE TABLE IF NOT EXISTS `labour_hiring` (
    labour_id INT,
    farmer_id INT,
    hiring_date DATE NOT NULL,
    no_of_days_worked INT NOT NULL,
    labour_cost DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (labour_id) REFERENCES labour(labour_id),
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;;

insert into `labour_hiring` values(1,1,DATE '2023-11-01',20,7000.00);


--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `name`) VALUES
(1, 'harshith');



--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(5, 'arkpro', 'arkpro@gmail.com', 'pbkdf2:sha256:150000$TfhDWqOr$d4cf40cc6cbfccbdcd1410f9e155ef2aa660620b0439a60c4d74085dbf007a4a');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `addagroproducts`
--
ALTER TABLE `addagroproducts`
  ADD PRIMARY KEY (`pid`);



--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trig`
--
ALTER TABLE `trig`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `addagroproducts`
--
ALTER TABLE `addagroproducts`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;





-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `trig`
--
ALTER TABLE `trig`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
