<?php
header('Access-Control-Allow-Origin: http://127.0.0.1:5500');

$servername = "localhost";
$username = "root";
$password = "CSC481_DevGrp7";
$dbname = "Menus";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT menu_id, menu_name FROM menu";
$result = $conn->query($sql);

$data = array();
if ($result->num_rows > 0) {
  while($row = $result->fetch_assoc()) {
    $data[] = $row;
  }
}


echo json_encode($data);

$conn->close();
?>
