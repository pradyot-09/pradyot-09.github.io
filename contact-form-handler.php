<?php

require("PHPMailer_5.2.0/class.phpmailer.php");
$name=$_POST['name'];
$email=$_POST['email'];
$phone=$_POST['phone'];
$msg=$_POST['msg'];
$mail = new PHPMailer;
$mail->setFrom('pradyot@paddi.ml');
$mail->addAddress("pradyotpatil@gmail.com");
$mail->Subject = "From: ".$email;
$mail->Body = "Name :".$name."\n"."Phone :".$phone."\n"."Wrote the following :"."\n\n".$msg;
//$mail->IsSMTP();
$mail->SMTPSecure = false ;
$mail->SMTPDebug = 2 ;
$mail->Host = 'ssl://smtp.gmail.com';
$mail->SMTPAuth = true;
$mail->Port = 465;

//Set your existing gmail address as user name
$mail->Username = 'vlabsteam@gmail.com';

//Set the password of your gmail address here
$mail->Password = 'gitlabiscool';
if(!$mail->send()) {
  echo 'Email is not sent.';
  echo 'Email error: ' . $mail->ErrorInfo;
} else {
  echo "<h1>Sent Successfully! Thank you"." ".$name.", I will contact you shortly!</h1>";
}

  ?>
