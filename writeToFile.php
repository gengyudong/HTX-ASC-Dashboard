<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the value from the AJAX request
    $value = $_POST['value'];

    // Write the value to a file
    file_put_contents('Output.txt', $value . PHP_EOL, FILE_APPEND);

    // Send a response back to the client
    echo 'Data written to file.';
}
?>