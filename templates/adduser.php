<?php
$id = $_POST['id'];
$name = $_POST['name'];
$rfid_uid = $_POST['rfid_uid'];

// Create connection
$conn = new mysqli('localhost', 'admin', 'password', 'Attended');
if ($conn->connect_error) {
    die('Connection Failed :' . $conn->connect_error);
} else {
    $result = $conn->prepare("INSERT INTO users (id,name,rfid_uid) VALUES (?,?,?)");
    $result->bind_param("isi", $id, $name, $rfid_uid);
    $result->execute();
    echo "Records added successfully.";
    $result->close();
    $conn->close();
}
?>