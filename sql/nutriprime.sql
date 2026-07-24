-- ==================================================
-- NutriPrimeKesehatan - Database Structure
-- Final Project Pemrograman Web
-- MariaDB / MySQL - SQL Native (tanpa ORM)
-- ==================================================

CREATE DATABASE IF NOT EXISTS nutriprimekesehatan
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE nutriprimekesehatan;

-- --------------------------------------------------
-- Tabel: users (khusus akun admin, bukan user publik)
-- --------------------------------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- --------------------------------------------------
-- Tabel: foods (database makanan & kandungan gizi)
-- --------------------------------------------------
CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    calories FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    fat FLOAT NOT NULL,
    carbs FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    image VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_food_name (name),
    INDEX idx_food_category (category)
) ENGINE=InnoDB;

-- --------------------------------------------------
-- Tabel: articles (artikel kesehatan, CRUD sederhana)
-- --------------------------------------------------
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    slug VARCHAR(180) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    thumbnail VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- --------------------------------------------------
-- Tabel: bmi_history (riwayat hasil kalkulator BMI)
-- --------------------------------------------------
CREATE TABLE bmi_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    height FLOAT NOT NULL,       -- cm
    weight FLOAT NOT NULL,       -- kg
    bmi_value FLOAT NOT NULL,
    category VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- --------------------------------------------------
-- Tabel: contacts (form kontak)
-- --------------------------------------------------
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==================================================
-- DUMMY DATA
-- ==================================================

-- Admin default
-- username: admin
-- password : admin123  (sudah di-hash pakai werkzeug.security.generate_password_hash)
INSERT INTO users (username, password) VALUES
('admin', 'scrypt:32768:8:1$RXa3kyGtvwXElXGY$2988b4d9e71af4e5c24d8da6c05296a184cab9eb341b194e2480e86c1161a9113c5ae8ea8aa23aa8badd3ca02010dec9f8e166995f4bc176f7f00d4017e950c3');

-- Data makanan
INSERT INTO foods (name, calories, protein, fat, carbs, category, description, image) VALUES
('Nasi Putih', 130, 2.7, 0.3, 28.0, 'Karbohidrat', 'Sumber karbohidrat utama masyarakat Indonesia, memberi energi cepat.', NULL),
('Dada Ayam Tanpa Kulit', 165, 31.0, 3.6, 0.0, 'Protein', 'Sumber protein tanpa lemak yang baik untuk pertumbuhan otot.', NULL),
('Telur Ayam Rebus', 155, 13.0, 11.0, 1.1, 'Protein', 'Sumber protein lengkap dengan asam amino esensial.', NULL),
('Brokoli', 34, 2.8, 0.4, 7.0, 'Sayur', 'Kaya serat, vitamin C, dan antioksidan.', NULL),
('Bayam', 23, 2.9, 0.4, 3.6, 'Sayur', 'Sayuran hijau tinggi zat besi dan folat.', NULL),
('Pisang', 89, 1.1, 0.3, 22.8, 'Buah', 'Sumber kalium dan energi cepat, cocok sebelum olahraga.', NULL),
('Apel', 52, 0.3, 0.2, 13.8, 'Buah', 'Buah rendah kalori tinggi serat, baik untuk pencernaan.', NULL),
('Tahu', 76, 8.0, 4.8, 1.9, 'Protein', 'Sumber protein nabati yang ekonomis dan rendah lemak jenuh.', NULL),
('Tempe', 193, 19.0, 11.0, 9.4, 'Protein', 'Hasil fermentasi kedelai, kaya protein dan probiotik alami.', NULL),
('Oatmeal', 68, 2.4, 1.4, 12.0, 'Karbohidrat', 'Sumber serat larut yang membantu menurunkan kolesterol.', NULL),
('Alpukat', 160, 2.0, 14.7, 8.5, 'Buah', 'Kaya lemak tak jenuh tunggal yang baik untuk jantung.', NULL),
('Ikan Salmon', 208, 20.0, 13.0, 0.0, 'Protein', 'Sumber omega-3 tinggi, baik untuk kesehatan jantung dan otak.', NULL);

-- Artikel kesehatan
INSERT INTO articles (title, slug, content, thumbnail) VALUES
('Pentingnya Menjaga Berat Badan Ideal', 'pentingnya-menjaga-berat-badan-ideal',
 'Berat badan ideal berperan penting dalam menjaga kesehatan jangka panjang. Kombinasi pola makan seimbang, aktivitas fisik rutin, dan istirahat cukup dapat membantu Anda mencapai dan mempertahankan berat badan yang sehat.', NULL),
('Memahami BMI dan Batasannya', 'memahami-bmi-dan-batasannya',
 'BMI (Body Mass Index) adalah indikator awal untuk menilai status berat badan seseorang berdasarkan tinggi dan berat badan. Meski praktis, BMI tidak membedakan massa otot dan lemak sehingga perlu dilengkapi pemeriksaan lain untuk hasil yang lebih akurat.', NULL),
('Tips Mengatur Kalori Harian', 'tips-mengatur-kalori-harian',
 'Mengetahui kebutuhan kalori harian melalui perhitungan BMR dan TDEE dapat membantu Anda menentukan target defisit atau surplus kalori sesuai tujuan, baik itu menurunkan berat badan, mempertahankan, maupun membangun massa otot.', NULL);

-- (bmi_history dan contacts dibiarkan kosong,
--  akan terisi otomatis saat aplikasi digunakan)
