-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 30, 2020 at 08:08 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_apps`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_af`
--

CREATE TABLE `tb_af` (
  `id` int(11) NOT NULL,
  `file` varchar(128) NOT NULL,
  `status_detect` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_af`
--

INSERT INTO `tb_af` (`id`, `file`, `status_detect`) VALUES
(1, 'test1-29112020-185509', 'Normal'),
(2, 'A00004-29112020-210436', 'Atrial Fibrilation'),
(3, 'A00001-30112020-165950', 'Normal'),
(4, 'A00001-30112020-175925', 'Normal'),
(5, 'A00001-30112020-180321', 'Normal'),
(6, 'test1-30112020-210933', 'Normal'),
(7, 'A00001-30112020-213625', 'Normal');

-- --------------------------------------------------------

--
-- Table structure for table `tb_arrdetect`
--

CREATE TABLE `tb_arrdetect` (
  `id` int(11) NOT NULL,
  `file` text NOT NULL,
  `status_detect` enum('0','1') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_af`
--
ALTER TABLE `tb_af`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_arrdetect`
--
ALTER TABLE `tb_arrdetect`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_af`
--
ALTER TABLE `tb_af`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tb_arrdetect`
--
ALTER TABLE `tb_arrdetect`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
