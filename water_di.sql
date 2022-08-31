-- phpMyAdmin SQL Dump
-- version 5.3.0-dev+20220817.de1eb66dbf
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 30, 2022 at 09:49 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.0.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `water_di`
--

-- --------------------------------------------------------

--
-- Table structure for table `di_error`
--

CREATE TABLE `di_error` (
  `Site` varchar(20) NOT NULL,
  `Detail` varchar(100) NOT NULL,
  `Date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `di_report`
--

CREATE TABLE `di_report` (
  `ID` int(11) NOT NULL,
  `Station` varchar(5) NOT NULL,
  `Phase` varchar(10) NOT NULL,
  `Site` varchar(20) NOT NULL,
  `Temp` float NOT NULL,
  `Water` float NOT NULL,
  `Date` date NOT NULL,
  `Time` time NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `log_status`
--

CREATE TABLE `log_status` (
  `Machine` varchar(50) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `Datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `machine`
--

CREATE TABLE `machine` (
  `ID` int(11) NOT NULL,
  `Machine` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `machine_data`
--

CREATE TABLE `machine_data` (
  `Site` varchar(20) NOT NULL,
  `Machine` varchar(50) NOT NULL,
  `Slot_Temp` int(3) NOT NULL,
  `Slot_Water` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `machine_master`
--

CREATE TABLE `machine_master` (
  `Machine` varchar(50) NOT NULL,
  `Ip` varchar(20) NOT NULL,
  `Port` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `machine_station`
--

CREATE TABLE `machine_station` (
  `ID` int(11) NOT NULL,
  `Station` varchar(5) NOT NULL,
  `Phase` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `off_set`
--

CREATE TABLE `off_set` (
  `Site` varchar(20) NOT NULL,
  `Low_Water` float NOT NULL,
  `Hight_Water` float NOT NULL,
  `Plus_Water` float NOT NULL,
  `Minus_Water` float NOT NULL,
  `Low_Temp` float NOT NULL,
  `Hight_Temp` float NOT NULL,
  `Plus_Temp` float NOT NULL,
  `Minus_Temp` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `op`
--

CREATE TABLE `op` (
  `OP` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `phase`
--

CREATE TABLE `phase` (
  `OP` varchar(5) NOT NULL,
  `Phase` varchar(10) NOT NULL,
  `Site` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pre_user`
--

CREATE TABLE `pre_user` (
  `Username` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `Username` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `di_error`
--
ALTER TABLE `di_error`
  ADD KEY `Site` (`Site`);

--
-- Indexes for table `di_report`
--
ALTER TABLE `di_report`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `log_status`
--
ALTER TABLE `log_status`
  ADD KEY `Machine` (`Machine`);

--
-- Indexes for table `machine`
--
ALTER TABLE `machine`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Machine` (`Machine`);

--
-- Indexes for table `machine_data`
--
ALTER TABLE `machine_data`
  ADD KEY `Site` (`Site`),
  ADD KEY `Machine` (`Machine`);

--
-- Indexes for table `machine_master`
--
ALTER TABLE `machine_master`
  ADD PRIMARY KEY (`Machine`);

--
-- Indexes for table `machine_station`
--
ALTER TABLE `machine_station`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `off_set`
--
ALTER TABLE `off_set`
  ADD PRIMARY KEY (`Site`);

--
-- Indexes for table `op`
--
ALTER TABLE `op`
  ADD PRIMARY KEY (`OP`);

--
-- Indexes for table `phase`
--
ALTER TABLE `phase`
  ADD KEY `OP` (`OP`),
  ADD KEY `Site` (`Site`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `di_report`
--
ALTER TABLE `di_report`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `machine`
--
ALTER TABLE `machine`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `machine_station`
--
ALTER TABLE `machine_station`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `di_error`
--
ALTER TABLE `di_error`
  ADD CONSTRAINT `di_error_ibfk_1` FOREIGN KEY (`Site`) REFERENCES `off_set` (`Site`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `log_status`
--
ALTER TABLE `log_status`
  ADD CONSTRAINT `log_status_ibfk_1` FOREIGN KEY (`Machine`) REFERENCES `machine_master` (`Machine`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `machine`
--
ALTER TABLE `machine`
  ADD CONSTRAINT `machine_ibfk_1` FOREIGN KEY (`Machine`) REFERENCES `machine_master` (`Machine`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `machine_data`
--
ALTER TABLE `machine_data`
  ADD CONSTRAINT `machine_data_ibfk_1` FOREIGN KEY (`Site`) REFERENCES `off_set` (`Site`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `machine_data_ibfk_2` FOREIGN KEY (`Machine`) REFERENCES `machine_master` (`Machine`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `phase`
--
ALTER TABLE `phase`
  ADD CONSTRAINT `phase_ibfk_1` FOREIGN KEY (`OP`) REFERENCES `op` (`OP`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `phase_ibfk_2` FOREIGN KEY (`Site`) REFERENCES `off_set` (`Site`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
