<?php
// توکن ربات خود را اینجا قرار دهید
$botToken = '6023368456:AAHGUL4ZTfGAG7MK1CqF_0pCTryQaQMjmlU';

// آیدی گروه یا چت خود را اینجا قرار دهید
$chatId = '-1001615937977';

// پیام خوش آمد گویی
$welcomeMessage = 'سلام! خوش آمدید به گروه ما.';

// API URL تلگرام
$telegramApiUrl = 'https://api.telegram.org/bot' . $botToken;

// تنظیمات پیام خوش آمد گویی
$welcomeMessageData = [
    'chat_id' => $chatId,
    'text' => $welcomeMessage,
];

// ارسال پیام خوش آمد گویی به کاربران تازه وارد
$response = file_get_contents($telegramApiUrl . '/sendMessage?' . http_build_query($welcomeMessageData));

// بررسی و پردازش پاسخ
if ($response) {
    $responseData = json_decode($response, true);
    if ($responseData['ok']) {
        echo 'پیام خوش آمد گویی با موفقیت ارسال شد.';
    } else {
        echo 'مشکلی در ارسال پیام به وجود آمده است: ' . $responseData['description'];
    }
} else {
    echo 'مشکلی در ارتباط با سرور تلگرام وجود دارد.';
}
?>
