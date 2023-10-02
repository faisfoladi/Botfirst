<?php
// PHP-Bibliothek für die Telegram Bot API verwenden
require_once 'TelegramBot.php'; // Stellen Sie sicher, dass Sie die entsprechende Bibliothek heruntergeladen haben.

// Ihr Telegram-Bot-Token
$botToken = '6023368456:AAHGUL4ZTfGAG7MK1CqF_0pCTryQaQMjmlU';

// Die ID Ihrer Telegram-Gruppe oder Ihres Kanals
$chatId = '-1001615937977';

// Nachricht, die an neue Mitglieder gesendet wird
$welcomeMessage = 'Herzlich willkommen in unserer Gruppe!';

// Initialisieren Sie den Bot
$bot = new TelegramBot($botToken);

// Holen Sie Updates von Telegram
$updates = $bot->getUpdates();

// Iterieren Sie durch neue Mitglieder und senden Sie die Willkommensnachricht
foreach ($updates as $update) {
    $message = $update->getMessage();
    if ($message->getNewMembers()) {
        foreach ($message->getNewMembers() as $newMember) {
            $userId = $newMember->getId();
            $bot->sendMessage($chatId, $welcomeMessage, $userId);
        }
    }
}
?>
