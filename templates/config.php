<?php
$conn = new mysqli('localhost', 'admin', 'password', 'Attended');
if ($conn->connect_error) {
    die('Connection Failed :' . $conn->connect_error);
} else {
    echo $mysqli->host_info . "\n";
}
?>