window.addEventListener('load', () => {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    // Save userId
    const userId = tg.initDataUnsafe.user?.id;
    if (userId) {
        localStorage.setItem("userId", userId);
        console.log("User ID сохранен:", userId);
    }

    // Detect language from Telegram OR fallback to 'uz'
    const userLang = tg.initDataUnsafe.user?.language_code || "ru";
    localStorage.setItem("lang", userLang);
    console.log("Language сохранен:", userLang);

    // Example: redirect to backend with lang param
    const backendUrl = `https://7ef19212fca3.ngrok-free.app?lang=ru`;
    document.getElementById("openDashboardBtn").addEventListener("click", () => {
        window.location.href = backendUrl;
    });
});
