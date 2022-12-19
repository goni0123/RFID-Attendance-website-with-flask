<?php
$Event_id = $_POST['Event_id'];
$Event_name = $_POST['Event_name'];
$Data_start= $_POST['Data_start'];
$Data_finish = $_POST['Data_finish'];
// Create connection
$conn = new mysqli('localhost', 'admin', 'password', 'Attended');
if ($conn->connect_error) {
    die('Connection Failed :' . $conn->connect_error);
} else {
    $result = $conn->prepare("INSERT INTO Event (Event_id, Event_name, Data_start,Data_finish) VALUES (?,?,?,?)");
    $result->bind_param("isss", $Event_id, $Event_name, $Data_start, $Data_finish);
    $result->execute();
    echo "Records added successfully.";
    $result->close();
    $conn->close();
}
?>