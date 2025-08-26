<?php
// Fake login handler for honeypot
// This captures credentials and redirects to error page

// Log the attempt
$logfile = '../data/logs/attacker_site.log';
$timestamp = date('Y-m-d H:i:s');
$ip = $_SERVER['REMOTE_ADDR'];
$user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

// Create log entry
$log_entry = json_encode([
    'timestamp' => $timestamp,
    'ip' => $ip,
    'user_agent' => $user_agent,
    'username' => $username,
    'password' => $password,
    'type' => 'fake_login_attempt'
]) . "\n";

// Ensure log directory exists
$log_dir = dirname($logfile);
if (!is_dir($log_dir)) {
    mkdir($log_dir, 0755, true);
}

// Write to log file
file_put_contents($logfile, $log_entry, FILE_APPEND | LOCK_EX);

// Simulate processing delay
sleep(2);

// Always show error message to maintain deception
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Error - SecureCorpNet</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        
        .error-icon {
            color: #dc3545;
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .error-title {
            color: #dc3545;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .error-message {
            color: #666;
            margin-bottom: 2rem;
            line-height: 1.5;
        }
        
        .back-btn {
            display: inline-block;
            padding: 0.75rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: transform 0.2s;
        }
        
        .back-btn:hover {
            transform: translateY(-2px);
        }
        
        .help-text {
            margin-top: 2rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 5px;
            font-size: 0.9rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">⚠️</div>
        <h2 class="error-title">Authentication Failed</h2>
        <p class="error-message">
            Invalid username or password. Please check your credentials and try again.
            <br><br>
            If you continue to experience issues, your account may be temporarily locked for security reasons.
        </p>
        <a href="index.html" class="back-btn">Try Again</a>
        
        <div class="help-text">
            <strong>Need Help?</strong><br>
            Contact IT Support: ext. 2847<br>
            Email: support@securecorpnet.com<br>
            Hours: Mon-Fri 8:00 AM - 6:00 PM
        </div>
    </div>
    
    <script>
        // Add some realistic behavior
        setTimeout(function() {
            console.log('Error logged');
        }, 1000);
    </script>
</body>
</html>
