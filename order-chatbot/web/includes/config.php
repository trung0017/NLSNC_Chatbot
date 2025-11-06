<?php
session_start();

define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'chatbot_db');

// API URL
define('API_URL', 'http://localhost:8000');

// Timezone
date_default_timezone_set('Asia/Ho_Chi_Minh');

// Error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1); 