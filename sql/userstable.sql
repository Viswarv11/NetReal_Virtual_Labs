-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 18, 2023 at 10:48 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vlabs`
--

-- --------------------------------------------------------

--
-- Table structure for table `userstable`
--

CREATE TABLE `userstable` (
  `FirstName` varchar(20) NOT NULL,
  `LastName` varchar(20) NOT NULL,
  `Mobile` bigint(10) NOT NULL,
  `Email` varchar(40) NOT NULL,
  `UserId` int(10) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Admin` int(1) NOT NULL DEFAULT 0,
  `coursefk` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `userstable`
--

INSERT INTO `userstable` (`FirstName`, `LastName`, `Mobile`, `Email`, `UserId`, `Password`, `Admin`, `coursefk`) VALUES
('viswa', 'r', 88234, 'viswa@gmail.com', 1, '123', 1, 0),
('Viswa', 'R', 888777666, 'v@gmail.com', 2, '123', 0, 0),
('SAM', 'ANTHA', 6666666, 'sam@gmail.com', 3, 'sam', 0, 0),
('Viswa', 'Ravichandran', 2147483647, 'viswar@gmail.com', 4, '1234', 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `userstable`
--
ALTER TABLE `userstable`
  ADD PRIMARY KEY (`UserId`),
  ADD KEY `coursefk` (`coursefk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `userstable`
--
ALTER TABLE `userstable`
  MODIFY `UserId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
