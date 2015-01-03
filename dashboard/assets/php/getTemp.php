<?php
    
$dbname = 'iot'; // Enter DB Here
$username = 'root'; // Enter Username Here
$password = 'root'; // Enter Password Here

$conn = new PDO("mysql:host=localhost;dbname=$dbname", $username, $password);
  $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

try {
  $result = $conn->query('SELECT *
		  FROM temperature
		  WHERE temperature.datetime > DATE_SUB(NOW(), INTERVAL 1 WEEK)
		  AND temperature.datetime <= NOW();');
  
  $rows = array();
  $table = array();
  $table['cols'] = array(array('label' => 'Datetime', 'type' => 'string'),array('label' => 'Temp', 'type' => 'number'));
    
  foreach($result as $r) {

  $data = array();
  $data[] = array('v' => (string) $r['datetime']); 
  $data[] = array('v' => (float) $r['temp']); 
      
  $rows[] = array('c' => $data);
  
  }

$table['rows'] = $rows;

} catch(PDOException $e) {
    echo 'ERROR: ' . $e->getMessage();
}

try {
  $result2 = $conn->prepare("SELECT `datetime`, `temp` from temperature
		  WHERE temperature.datetime > DATE_SUB(NOW(), INTERVAL 1 HOUR)
		  AND temperature.datetime <= NOW();");
		  
  $result2->execute();

} catch(PDOException $e) {
    echo 'ERROR: ' . $e->getMessage();
}
	
?>
