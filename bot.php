<?php
// Telegram Bot-Token
$botToken = '6023368456:AAH1VbbHH7_6nW1lb2BoETdahGuhJufhU_o';

// ID der Zielgruppe oder des Chats
$chatId = '-1001615937977';

// URL für die Telegram Bot-API
$telegramApiUrl = "https://api.telegram.org/bot$botToken";

// Verarbeite den eingehenden Update von Telegram
$update = json_decode(file_get_contents("php://input"), true);

// Überprüfe, ob das Update Daten enthält
if (isset($update['message'])) {
    $message = $update['message'];
    $userId = $message['from']['id'];

    // Willkommensnachricht, wenn ein neuer Benutzer beitritt
    if (isset($message['new_chat_members'])) {
        foreach ($message['new_chat_members'] as $newMember) {
            $welcomeMessage = "Willkommen, {$newMember['first_name']}!";
            sendMessage($chatId, $welcomeMessage);
        }
    }

    // Hallo-Nachricht beantworten
    if (isset($message['text']) && strtolower($message['text']) == 'hallo') {
        $response = "Hallo, {$message['from']['first_name']}!";
        sendMessage($chatId, $response);
    }

    // Sperrung eines Benutzers
    if (isset($message['text']) && strtolower($message['text']) == '/sperren' && $userId == 'DEINE_BENUTZER_ID') {
        $userToBanId = $message['reply_to_message']['from']['id'];
        kickUser($chatId, $userToBanId);
    }

    // Stummschaltung eines Benutzers
    if (isset($message['text']) && strtolower($message['text']) == '/stumm' && $userId == 'DEINE_BENUTZER_ID') {
        $userToMuteId = $message['reply_to_message']['from']['id'];
        muteUser($chatId, $userToMuteId);
    }
}

// Funktion zum Senden von Nachrichten
function sendMessage($chatId, $text) {
    global $telegramApiUrl;
    $params = [
        'chat_id' => $chatId,
        'text' => $text,
    ];
    file_get_contents("$telegramApiUrl/sendMessage?" . http_build_query($params));
}

// Funktion zum Sperren eines Benutzers
function kickUser($chatId, $userId) {
    global $telegramApiUrl;
    $params = [
        'chat_id' => $chatId,
        'user_id' => $userId,
    ];
    file_get_contents("$telegramApiUrl/kickChatMember?" . http_build_query($params));
}

// Funktion zum Stummschalten eines Benutzers
function muteUser($chatId, $userId) {
    global $telegramApiUrl;
    $params = [
        'chat_id' => $chatId,
        'user_id' => $userId,
        'until_date' => strtotime('+1 day'), // Stummschaltung für 1 Tag
    ];
    file_get_contents("$telegramApiUrl/restrictChatMember?" . http_build_query($params));
}
?>
