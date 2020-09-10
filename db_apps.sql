-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2020 at 10:33 AM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
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
-- Table structure for table `tb_arrdetect`
--

CREATE TABLE `tb_arrdetect` (
  `id_detect` int(11) NOT NULL,
  `file` varchar(255) NOT NULL,
  `status_detect` enum('0','1') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_arrdetect`
--

INSERT INTO `tb_arrdetect` (`id_detect`, `file`, `status_detect`) VALUES
(1, '123', '1'),
(2, '1111', '1'),
(3, '1233', '0'),
(4, 'WhatsApp_Image_2020-09-08_at_13.55.49.jpeg', '0');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_arrdetect`
--
ALTER TABLE `tb_arrdetect`
  ADD PRIMARY KEY (`id_detect`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_arrdetect`
--
ALTER TABLE `tb_arrdetect`
  MODIFY `id_detect` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
