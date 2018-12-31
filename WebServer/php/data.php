<?php

//getting data from database
$conn = mysqli_connect("192.168.43.240", "Lin", "123456", "SenseData");

//getting data from sensedata table
//get the lastest 50 data
$result = mysqli_query($conn, "SELECT * FROM sensedata order by time desc limit 50");

//storing data in array
$data = array();
while ($row = mysqli_fetch_assoc($result))
{
	$data[] = $row;
}

//returning respons in JSON format
echo json_encode($data);

?>
