<?php
// تنظیمات
$botToken = '6023368456:AAH1VbbHH7_6nW1lb2BoETdahGuhJufhU_o'; // توکن ربات خود را اینجا قرار دهید
$chatId = '-1001615937977'; // آیدی گروه یا چت مورد نظرتان را اینجا قرار دهید

// اطلاعات مربوط به درخواست
$update = json_decode(file_get_contents('php://input'), true);
$message = $update['message'];
$userId = $message['from']['id'];
$chatType = $message['chat']['type'];

// تابع ارسال پیام به تلگرام
function sendMessage($chatId, $text) {
    global $botToken;
    $url = "https://api.telegram.org/bot$botToken/sendMessage";
    $data = http_build_query(['chat_id' => $chatId, 'text' => $text]);
    file_get_contents("$url?$data");
}

// دستور خوش آمد گویی به اعضای جدید
if ($message['new_chat_members'] && $chatType === 'supergroup') {
    foreach ($message['new_chat_members'] as $newMember) {
        $welcomeMessage = "سلام {$newMember['first_name']} عزیز! خوش آمدید به گروه ما.";
        sendMessage($chatId, $welcomeMessage);
    }
}

// دستور افزودن ادمین
if ($message['text'] === 'اضافه کردن ادمین' && $userId === YOUR_ADMIN_USER_ID) {
    // در اینجا کد برای اضافه کردن ادمین را اضافه کنید
    sendMessage($chatId, 'کاربر به عنوان ادمین افزوده شد.');
}

// دستور اخراج کاربر
if ($message['text'] === 'اخراج کاربر' && $userId === YOUR_ADMIN_USER_ID) {
    // در اینجا کد برای اخراج کاربر را اضافه کنید
    sendMessage($chatId, 'کاربر از گروه اخراج شد.');
}

// دستور بی صدا کردن کاربر
if ($message['text'] === 'بی صدا کردن کاربر' && $userId === YOUR_ADMIN_USER_ID) {
    // در اینجا کد برای بی صدا کردن کاربر را اضافه کنید
    sendMessage($chatId, 'کاربر به حالت بی صدا درآمد.');
}

// دستور آزاد کردن کاربر از بی صدا و اخراج
if ($message['text'] === 'آزاد کردن کاربر' && $userId === YOUR_ADMIN_USER_ID) {
    // در اینجا کد برای آزاد کردن کاربر از بی صدا و اخراج را اضافه کنید
    sendMessage($chatId, 'کاربر از اخراج و حالت بی صدا خارج شد.');
}
?>
