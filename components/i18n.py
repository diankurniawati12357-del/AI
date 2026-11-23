"""Centralized BIOVA interface translations."""

import streamlit as st
from services.db import get_connection


ID = {
    "welcome.headline": "Jelajahi Sekitarmu!",
    "welcome.subtitle": "Temukan, Kenali, & Pelajari.",
    "welcome.description": "Jelajahi keanekaragaman hayati bersama BIOVA, teman belajar alam berbasis AI.",
    "welcome.start": "Mulai Petualangan",
    "welcome.login": "Masuk",
    "welcome.register": "Daftar Akun",
    "auth.login": "Masuk",
    "auth.register": "Daftar",
    "auth.username": "Nama Pengguna",
    "auth.password": "Kata Sandi",
    "auth.username_placeholder": "Masukkan nama pengguna",
    "auth.password_placeholder": "Masukkan kata sandi",
    "auth.welcome": "Selamat Datang Kembali!",
    "auth.continue": "Lanjutkan petualanganmu bersama BIOVA",
    "auth.google": "Lanjutkan dengan Google",
    "auth.or": "atau",
    "auth.no_account": "Belum punya akun?",
    "auth.has_account": "Sudah punya akun?",
    "auth.register_headline": "Petualanganmu Dimulai di Sini!",
    "auth.register_subtitle": "Yuk, ambil langkah pertamamu bersama BIOVA",
    "auth.create_account": "Buat akun BIOVA",
    "auth.register_now": "Daftar Sekarang",
    "auth.goto_login": "Masuk ke Akunmu",
    "auth.email_placeholder": "contoh: nama@mhs.unesa.ac.id",
    "auth.username_hint": "Pilih nama pengguna (min. 3 huruf)",
    "auth.password_hint": "Minimal 6 karakter",
    "auth.google_not_configured": "Login Google belum dikonfigurasi. Gunakan nama pengguna dan kata sandi.",
    "auth.google_unavailable": "Konfigurasi Google OAuth belum tersedia pada aplikasi ini.",
    "nav.back": "Kembali",
    "nav.dashboard": "Beranda",
    "nav.learn": "Belajar",
    "nav.leaderboard": "Peringkat",
    "nav.profile": "Profil",
    "leaderboard.title": "Papan Peringkat",
    "stars.my": "Bintang Saya",
    "header.welcome": "Selamat Datang Kembali,",
    "profile.edit_photo": "Ubah Foto Profil",
    "profile.save_photo": "Simpan Perubahan",
    "profile.cancel": "Batal",
    "profile.remove_photo": "Hapus Foto",
    "profile.completed_material": "Materi Selesai",
    "profile.completed_quiz": "Kuis Selesai",
    "profile.rank": "Peringkat",
    "learn.title": "Ayo, Belajar Bersama!",
    "learn.subtitle": "Kumpulkan kartu dan temukan alam di sekitarmu.",
    "learn.progress": "Progres",
    "learn.completed": "Selesai",
    "learn.open": "Pelajari",
    "quiz.check": "Cek Jawaban",
    "quiz.next": "Berikutnya",
    "quiz.result": "Lihat Hasil Kuis",
    "scan.upload_animal": "Unggah Gambar Hewan",
    "scan.upload_plant": "Unggah Gambar Tumbuhan",
    "scan.identify": "Identifikasi AI",
    "welcome.category_prompt": "Pilih kategori untuk mengenali flora dan fauna di kampus UNESA:",
    "category.animals": "Hewan",
    "category.plants": "Tumbuhan",
    "category.animals_description": "Kenali berbagai jenis hewan di sekitarmu melalui foto satwa.",
    "category.plants_description": "Kenali keanekaragaman tumbuhan di sekitarmu melalui foto daun atau pohon.",
    "home.explore_animals": "Yuk, Jelajahi Dunia Hewan!",
    "home.explore_plants": "Yuk, Jelajahi Tumbuhan di UNESA!",
    "learn.animal_description": "Pelajari 6 kelompok fauna (Mamalia, Aves, Reptil, Amfibi, Pisces, Invertebrata) dan habitatnya di UNESA.",
    "learn.plant_description": "Pelajari perbedaan Dikotil dan Monokotil, pohon peneduh kampus, serta fungsi ekologis flora UNESA.",
    "learn.animal_material": "Materi Hewan",
    "learn.animal_quiz": "Kuis Hewan",
    "learn.plant_material": "Materi Tumbuhan",
    "learn.plant_quiz": "Kuis Tumbuhan",
    "learn.selected_category": "Kategori pilihan: {category}",
    "learn.progress_format": "Progres: {completed}/{total} Materi Selesai",
    "lesson.previous": "Sebelumnya",
    "lesson.next": "Berikutnya",
    "lesson.collection": "Koleksi Materi {category}",
    "lesson.mark_complete": "Tandai Materi Selesai",
    "lesson.completed": "Materi Selesai",
    "lesson.collection_brand": "BIOVA NATURE COLLECTION",
    "lesson.card_number": "CARD",
    "lesson.flip_to_back": "Balik Kartu",
    "lesson.flip_to_front": "Balik Kembali",
    "lesson.did_you_know": "Tahukah Kamu?",
    "lesson.fun_fact": "Fakta Menarik",
    "lesson.examples": "Contoh",
    "lesson.flip_card_alt": "Kartu materi interaktif: {title}",
    "collection.flip": "Balik Kartu",
    "collection.return": "Balik Kembali",
    "collection.overview": "Ringkasan",
    "lesson.no_data": "Data materi tidak ditemukan.",
    "lesson.preparing": "Materi ini sedang disiapkan.",
    "quiz.title": "Kuis {category}",
    "quiz.question": "Soal {current} dari {total}",
    "quiz.choose": "Pilih jawabanmu:",
    "quiz.choose_warning": "Silakan pilih salah satu jawaban terlebih dahulu.",
    "quiz.correct": "Jawabanmu Benar!",
    "quiz.incorrect": "Jawabanmu Kurang Tepat.",
    "quiz.correct_answer": "Jawaban yang benar adalah:",
    "quiz.discussion": "Pembahasan:",
    "quiz.exit": "Keluar Kuis",
    "quiz.unavailable": "Bank soal kuis belum tersedia atau belum memiliki lima soal bilingual yang valid.",
    "quiz.great": "KAMU HEBAT!",
    "quiz.completed": "Kamu telah menyelesaikan Kuis {category}.",
    "quiz.correct_answers": "Jawaban Benar",
    "quiz.stars_won": "Bintang Diperoleh",
    "quiz.final_score": "Skor Akhir",
    "quiz.back_material": "Kembali ke Materi",
    "quiz.perfect_bonus": "Bonus Sempurna +3",
    "quiz.keep_improving": "Terus Tingkatkan!",
    "quiz.current_rank": "Posisi Peringkatmu Saat Ini:",
    "quiz.top_leaderboard": "Papan Peringkat Teratas:",
    "quiz.back_home": "Kembali ke Beranda",
    "quiz.repeat": "Ulangi Kuis",
    "leaderboard.subtitle": "Petualang alam dengan perolehan bintang terbanyak di BIOVA:",
    "leaderboard.empty": "Belum ada data petualang di papan peringkat.",
    "leaderboard.you": "(Kamu)",
    "leaderboard.my_rank": "Peringkat Saya",
    "leaderboard.previous": "Sebelumnya",
    "leaderboard.next": "Berikutnya",
    "profile.tier": "Tingkat Petualang",
    "profile.activity": "Aktivitas Eksplorasi",
    "profile.verified_photos": "Foto Berhasil Terverifikasi:",
    "profile.quizzes_taken": "Kuis Dikerjakan:",
    "profile.logout": "Keluar dari Akun",
    "profile.next_tier": "Kumpulkan {stars} bintang lagi untuk naik tier!",
    "profile.top_tier": "Kamu sudah mencapai tier tertinggi!",
    "common.total_stars": "Total Bintang",
    "common.home": "Beranda",
    "common.animals": "Hewan",
    "common.plants": "Tumbuhan",
    "common.upload": "Unggah",
    "common.camera": "Ambil Foto",
    "common.identify": "Identifikasi",
    "panorama.title": "Buat Panorama dari Fotomu!",
    "panorama.description": "Gabungkan beberapa foto menjadi satu pemandangan indah.",
    "panorama.start": "Mulai Buat Panorama",
}

EN = {
    "welcome.headline": "Explore the Nature Around You!",
    "welcome.subtitle": "Discover, Identify & Learn.",
    "welcome.description": "Explore biodiversity with BIOVA, your AI-powered nature learning companion.",
    "welcome.start": "Start the Adventure",
    "welcome.login": "Sign In",
    "welcome.register": "Create Account",
    "auth.login": "Sign In",
    "auth.register": "Sign Up",
    "auth.username": "Username",
    "auth.password": "Password",
    "auth.username_placeholder": "Enter username",
    "auth.password_placeholder": "Enter password",
    "auth.welcome": "Welcome Back!",
    "auth.continue": "Continue your adventure with BIOVA",
    "auth.google": "Continue with Google",
    "auth.or": "or",
    "auth.no_account": "Don't have an account?",
    "auth.has_account": "Already have an account?",
    "auth.register_headline": "Your Adventure Starts Here!",
    "auth.register_subtitle": "Take your first step with BIOVA",
    "auth.create_account": "Create a BIOVA Account",
    "auth.register_now": "Create Account",
    "auth.goto_login": "Sign In",
    "auth.email_placeholder": "example: name@unesa.ac.id",
    "auth.username_hint": "Choose a username (min. 3 characters)",
    "auth.password_hint": "Minimum 6 characters",
    "auth.google_not_configured": "Google login is not configured. Use your username and password.",
    "auth.google_unavailable": "Google OAuth configuration is not available in this app.",
    "nav.back": "Back",
    "nav.dashboard": "Home",
    "nav.learn": "Learn",
    "nav.leaderboard": "Leaderboard",
    "nav.profile": "Profile",
    "leaderboard.title": "Leaderboard",
    "stars.my": "My Stars",
    "scan.upload_animal": "Upload Animal Image",
    "scan.upload_plant": "Upload Plant Image",
    "scan.identify": "AI Identification",
    "header.welcome": "Welcome Back,",
    "profile.edit_photo": "Change Profile Photo",
    "profile.save_photo": "Save Changes",
    "profile.cancel": "Cancel",
    "profile.remove_photo": "Remove Photo",
    "profile.completed_material": "Materials Completed",
    "profile.completed_quiz": "Quizzes Completed",
    "profile.rank": "Rank",
    "learn.title": "Let's Learn Together!",
    "learn.subtitle": "Collect cards and discover nature around you.",
    "learn.progress": "Progress",
    "learn.completed": "Completed",
    "learn.open": "Learn",
    "quiz.check": "Check Answer",
    "quiz.next": "Next",
    "quiz.result": "View Quiz Result",
    "welcome.category_prompt": "Choose a category to identify flora and fauna at UNESA:",
    "category.animals": "Animals",
    "category.plants": "Plants",
    "category.animals_description": "Identify animals around you through photos.",
    "category.plants_description": "Identify plant diversity around you through leaf or tree photos.",
    "home.explore_animals": "Explore the World of Animals!",
    "home.explore_plants": "Explore UNESA's Plants!",
    "learn.animal_description": "Learn about 6 animal groups (Mammals, Birds, Reptiles, Amphibians, Fish, and Invertebrates) and their habitats at UNESA.",
    "learn.plant_description": "Learn the differences between dicots and monocots, campus shade trees, and the ecological roles of UNESA plants.",
    "learn.animal_material": "Animal Materials",
    "learn.animal_quiz": "Animal Quiz",
    "learn.plant_material": "Plant Materials",
    "learn.plant_quiz": "Plant Quiz",
    "learn.selected_category": "Selected category: {category}",
    "learn.progress_format": "Progress: {completed}/{total} Materials Completed",
    "lesson.previous": "Previous",
    "lesson.next": "Next",
    "lesson.collection": "{category} Learning Collection",
    "lesson.mark_complete": "Mark Material as Complete",
    "lesson.completed": "Material Completed",
    "lesson.collection_brand": "BIOVA NATURE COLLECTION",
    "lesson.card_number": "CARD",
    "lesson.flip_to_back": "Flip Card",
    "lesson.flip_to_front": "Tap to return",
    "lesson.did_you_know": "Did You Know?",
    "lesson.fun_fact": "Fun Fact",
    "lesson.examples": "Examples",
    "lesson.flip_card_alt": "Interactive material card: {title}",
    "collection.flip": "Flip Card",
    "collection.return": "Tap to return",
    "collection.overview": "Overview",
    "lesson.no_data": "Learning material data was not found.",
    "lesson.preparing": "This material is being prepared.",
    "quiz.title": "{category} Quiz",
    "quiz.question": "Question {current} of {total}",
    "quiz.choose": "Choose your answer:",
    "quiz.choose_warning": "Please choose one answer first.",
    "quiz.correct": "Your Answer Is Correct!",
    "quiz.incorrect": "Your Answer Is Not Quite Right.",
    "quiz.correct_answer": "The correct answer is:",
    "quiz.discussion": "Explanation:",
    "quiz.exit": "Exit Quiz",
    "quiz.unavailable": "The quiz bank is unavailable or has fewer than five valid bilingual questions.",
    "quiz.great": "YOU'RE AMAZING!",
    "quiz.completed": "You completed the {category} Quiz.",
    "quiz.correct_answers": "Correct Answers",
    "quiz.stars_won": "Stars Earned",
    "quiz.final_score": "Final Score",
    "quiz.back_material": "Back to Materials",
    "quiz.perfect_bonus": "Perfect Bonus +3",
    "quiz.keep_improving": "Keep Improving!",
    "quiz.current_rank": "Your Current Rank:",
    "quiz.top_leaderboard": "Top Leaderboard:",
    "quiz.back_home": "Back to Home",
    "quiz.repeat": "Retry Quiz",
    "leaderboard.subtitle": "Nature explorers with the most stars earned in BIOVA:",
    "leaderboard.empty": "There is no explorer data on the leaderboard yet.",
    "leaderboard.you": "(You)",
    "leaderboard.my_rank": "My Rank",
    "leaderboard.previous": "Previous",
    "leaderboard.next": "Next",
    "profile.tier": "Explorer Tier",
    "profile.activity": "Exploration Activity",
    "profile.verified_photos": "Successfully Verified Photos:",
    "profile.quizzes_taken": "Quizzes Completed:",
    "profile.logout": "Log Out",
    "profile.next_tier": "Collect {stars} more stars to reach the next tier!",
    "profile.top_tier": "You have reached the highest tier!",
    "common.total_stars": "Total Stars",
    "common.home": "Home",
    "common.animals": "Animals",
    "common.plants": "Plants",
    "common.upload": "Upload",
    "common.camera": "Take Photo",
    "common.identify": "Identify",
    "panorama.title": "Make a Panorama from Your Photos!",
    "panorama.description": "Combine photos into a beautiful landscape.",
    "panorama.start": "Start Panorama",
}

LANGUAGES = {"id": "Bahasa Indonesia", "en": "English"}


def init_language():
    if "language" not in st.session_state:
        user = st.session_state.get("authenticated_user")
        preferred = "id"
        if user:
            preferred = str(user.get("language") or "id").lower()
            if preferred not in ("id", "en"):
                preferred = "id"
        st.session_state["language"] = preferred
    return st.session_state["language"]


def set_language(language: str) -> str:
    language = str(language).lower()
    if language not in ("id", "en"):
        language = "id"
    if st.session_state.get("language") != language:
        st.session_state["_language_widget_revision"] = (
            int(st.session_state.get("_language_widget_revision", 0)) + 1
        )
    st.session_state["language"] = language
    st.session_state["_language_explicit"] = True
    user = st.session_state.get("authenticated_user")
    if user:
        try:
            with get_connection() as conn:
                conn.execute("UPDATE users SET language = ? WHERE id = ?;", (language, user["id"]))
                conn.commit()
            user["language"] = language
        except Exception:
            pass
    return language


def t(key: str, fallback: str | None = None) -> str:
    language = init_language()
    dictionary = ID if language == "id" else EN
    if key in dictionary:
        return dictionary[key]
    if fallback is not None:
        return fallback
    return ID.get(key, EN.get(key, key))


MATERIAL_EN = {
    "Mamalia": ("Mammals", "Vertebrates that produce milk to feed their young; most have hair or fur.", "Breathe with lungs and are warm-blooded; most give birth to live young."),
    "Aves": ("Birds (Aves)", "Warm-blooded vertebrates with feathers, wings, and a beak.", "Lay eggs and breathe with lungs supported by air sacs."),
    "Reptilia": ("Reptiles", "Vertebrates with dry, keratin-covered scales that help reduce water loss.", "Breathe with lungs; body temperature depends largely on the environment."),
    "Amfibi": ("Amphibians", "Vertebrates whose life cycle commonly includes aquatic larvae and a terrestrial adult stage.", "Have moist, permeable skin and generally undergo metamorphosis."),
    "Pisces": ("Fish", "Aquatic vertebrates that use gills to take oxygen from water.", "Use fins to move and stabilize their bodies in water."),
    "Invertebrata": ("Invertebrates", "Animals that do not have a vertebral column.", "Include many groups, such as insects, worms, and mollusks."),
    "Struktur Biji & Keping (Kotiledon)": ("Seed and Cotyledon Structure", "Monocots have one seed leaf while dicots have two.", "The cotyledons store nutrients for early seedling growth."),
    "Sistem Perakaran": ("Root Systems", "Monocots commonly have fibrous roots, while dicots commonly develop a main taproot.", "Roots anchor plants and absorb water and minerals from the soil."),
    "Struktur & Tulang Daun": ("Leaf Structure and Venation", "Monocot leaves commonly have parallel veins; dicot leaves commonly have netted veins.", "Leaves capture light and exchange gases for photosynthesis."),
    "Struktur Batang & Kambium": ("Stem and Cambium Structure", "Dicot stems contain cambium and may grow wider; monocot vascular bundles are scattered.", "Cambium supports secondary woody growth."),
    "Struktur Bunga": ("Flower Structure", "Monocot flowers commonly have parts in threes; dicot flowers commonly have parts in fours or fives.", "Flowers contain reproductive structures and attract pollinators."),
}

MATERIAL_FLIP_COPY = {
    "hewan": {
        "mamalia": {
            "id": ("Mamalia adalah hewan yang menyusui anaknya.", "Kancil juga termasuk mamalia, lho! Kelelawar pun mamalia meskipun bisa terbang.", "Kancil, gajah, kucing."),
            "en": ("Mammals are animals that feed their young with milk.", "Mouse-deer are mammals too! Bats are mammals, even though they can fly.", "Mouse-deer, elephants, cats."),
        },
        "aves": {
            "id": ("Burung memiliki paruh, sayap, dan tubuh berbulu.", "Burung unta tidak bisa terbang, tetapi bisa berlari sangat cepat!", "Ayam, merpati, burung unta."),
            "en": ("Birds have beaks, wings, and feather-covered bodies.", "Ostriches cannot fly, but they can run very fast!", "Chickens, pigeons, ostriches."),
        },
        "reptilia": {
            "id": ("Reptil umumnya memiliki kulit bersisik.", "Ular dan kura-kura sama-sama reptil meskipun bentuk tubuhnya berbeda.", "Ular, kadal, kura-kura."),
            "en": ("Reptiles generally have scaly skin.", "Snakes and turtles are both reptiles, even though their body shapes differ.", "Snakes, lizards, turtles."),
        },
        "amfibi": {
            "id": ("Amfibi biasanya mengalami fase hidup di air dan di darat.", "Saat menjadi kecebong, katak bernapas menggunakan insang!", "Katak, kodok, salamander."),
            "en": ("Amphibians usually have life stages in water and on land.", "As tadpoles, frogs breathe using gills!", "Frogs, toads, salamanders."),
        },
        "pisces": {
            "id": ("Ikan adalah hewan air yang umumnya bernapas dengan insang.", "Ikan badut dapat hidup berdampingan dengan anemon laut.", "Ikan badut, ikan nila, ikan mas."),
            "en": ("Fish are aquatic animals that generally breathe through gills.", "Clownfish can live alongside sea anemones.", "Clownfish, tilapia, goldfish."),
        },
        "invertebrata": {
            "id": ("Invertebrata adalah hewan tanpa tulang belakang.", "Gurita dan kupu-kupu sama-sama tidak memiliki tulang belakang!", "Gurita, semut, kupu-kupu."),
            "en": ("Invertebrates are animals without a backbone.", "Octopuses and butterflies both have no backbone!", "Octopuses, ants, butterflies."),
        },
    },
    "tumbuhan": {
        "biji_keping": {
            "id": ("Monokotil memiliki satu keping biji, sedangkan dikotil memiliki dua.", "Jagung termasuk monokotil, sedangkan kacang tanah termasuk dikotil!", "Jagung dan kacang tanah."),
            "en": ("Monocots have one seed leaf, while dicots have two.", "Corn is a monocot, while peanuts are dicots!", "Corn and peanuts."),
        },
        "sistem_perakaran": {
            "id": ("Monokotil biasanya berakar serabut, sedangkan dikotil umumnya berakar tunggang.", "Akar pohon mangga dapat tumbuh kuat dan membantu menopang pohon!", "Padi dan mangga."),
            "en": ("Monocots usually have fibrous roots, while dicots commonly have a taproot.", "Mango tree roots can grow strong and help support the tree!", "Rice and mango."),
        },
        "tulang_daun": {
            "id": ("Tulang daun dapat berbentuk sejajar, menyirip, atau menjari.", "Daun pisang memiliki pola tulang hampir sejajar, sedangkan mangga menyirip!", "Pisang dan mangga."),
            "en": ("Leaf veins can be parallel, pinnate, or palmate.", "Banana leaves have nearly parallel veins, while mango leaves have pinnate veins!", "Banana and mango."),
        },
        "batang_kambium": {
            "id": ("Batang menopang tumbuhan dan menyalurkan air serta zat makanan.", "Banyak tumbuhan dikotil memiliki kambium yang membuat batang membesar!", "Mangga dan jagung."),
            "en": ("Stems support plants and transport water and nutrients.", "Many dicots have cambium that makes their stems grow wider!", "Mango and corn."),
        },
        "struktur_bunga": {
            "id": ("Bunga berperan dalam reproduksi tumbuhan berbunga.", "Bagian bunga monokotil biasanya berkelipatan tiga, sedangkan dikotil sering empat atau lima!", "Lili dan kembang sepatu."),
            "en": ("Flowers play a role in the reproduction of flowering plants.", "Monocot flower parts are usually in threes, while dicot parts are often in fours or fives!", "Lilies and hibiscus."),
        },
    },
}

COLLECTION_FLIP_COPY = {
    "hewan": {
        "mamalia": {
            "id": ("Hewan yang menyusui anaknya dan umumnya memiliki rambut atau bulu.", "Kancil dan kelelawar sama-sama mamalia, lho!", "Kancil, kucing, gajah."),
            "en": ("Animals that nurse their young and usually have hair or fur.", "Mouse-deer and bats are both mammals!", "Mouse-deer, cats, elephants."),
        },
        "aves": {
            "id": ("Kelompok burung yang memiliki paruh, sayap, dan bulu.", "Burung unta tidak bisa terbang, tetapi jago berlari!", "Ayam, merpati, burung unta."),
            "en": ("Birds have beaks, wings, and feathers.", "Ostriches cannot fly, but they are excellent runners!", "Chickens, pigeons, ostriches."),
        },
        "reptilia": {
            "id": ("Hewan bertulang belakang yang umumnya memiliki kulit bersisik.", "Ular dan kura-kura ternyata masih satu kelompok reptil!", "Ular, kadal, kura-kura."),
            "en": ("Vertebrates that generally have scaly skin.", "Snakes and turtles are both reptiles!", "Snakes, lizards, turtles."),
        },
        "amfibi": {
            "id": ("Hewan yang biasanya mengalami fase hidup di air dan darat.", "Katak bernapas dengan insang saat masih menjadi kecebong!", "Katak, kodok, salamander."),
            "en": ("Animals that usually have life stages in water and on land.", "Frogs breathe through gills as tadpoles!", "Frogs, toads, salamanders."),
        },
        "pisces": {
            "id": ("Kelompok ikan yang hidup di air dan umumnya bernapas dengan insang.", "Ikan badut dapat hidup berdampingan dengan anemon laut!", "Ikan badut, ikan nila, ikan mas."),
            "en": ("Fish live in water and generally breathe through gills.", "Clownfish can live alongside sea anemones!", "Clownfish, tilapia, goldfish."),
        },
        "invertebrata": {
            "id": ("Hewan yang tidak memiliki tulang belakang.", "Gurita dan kupu-kupu sama-sama invertebrata!", "Gurita, kupu-kupu, semut."),
            "en": ("Animals that do not have a backbone.", "Octopuses and butterflies are both invertebrates!", "Octopuses, butterflies, ants."),
        },
    },
    "tumbuhan": {
        "biji_keping": {
            "id": ("Monokotil memiliki satu keping biji, sedangkan dikotil memiliki dua.", "Jagung termasuk monokotil, sedangkan kacang tanah termasuk dikotil!", "Jagung dan kacang tanah."),
            "en": ("Monocots have one cotyledon, while dicots have two.", "Corn is a monocot, while peanuts are dicots!", "Corn and peanuts."),
        },
        "sistem_perakaran": {
            "id": ("Monokotil umumnya berakar serabut dan dikotil biasanya berakar tunggang.", "Akar mangga bisa tumbuh kuat untuk menopang pohon!", "Padi dan mangga."),
            "en": ("Monocots generally have fibrous roots, while dicots usually have taproots.", "Mango roots can grow strong to support the tree!", "Rice and mango."),
        },
        "tulang_daun": {
            "id": ("Tulang daun dapat berbentuk sejajar, menyirip, atau menjari.", "Daun pisang berpola hampir sejajar, sedangkan daun mangga menyirip!", "Pisang dan mangga."),
            "en": ("Leaf veins can be parallel, pinnate, or palmate.", "Banana leaves have nearly parallel veins, while mango leaves have pinnate veins!", "Banana and mango."),
        },
        "batang_kambium": {
            "id": ("Batang menopang tumbuhan dan membantu mengalirkan air serta nutrisi.", "Banyak tumbuhan dikotil punya kambium yang membuat batang membesar!", "Mangga dan jagung."),
            "en": ("Stems support plants and help transport water and nutrients.", "Many dicots have cambium that makes their stems grow wider!", "Mango and corn."),
        },
        "struktur_bunga": {
            "id": ("Bunga berperan dalam reproduksi tumbuhan berbunga.", "Bunga monokotil umumnya memiliki bagian berkelipatan tiga!", "Lili dan kembang sepatu."),
            "en": ("Flowers play a role in the reproduction of flowering plants.", "Monocot flowers usually have parts in multiples of three!", "Lilies and hibiscus."),
        },
    },
}


def get_material_flip_copy(category: str, material_id: str) -> dict:
    """Return concise bilingual flip-card copy by stable category and material ID."""
    language = init_language()
    content = MATERIAL_FLIP_COPY.get(category, {}).get(material_id)
    if not content:
        raise KeyError(f"No flip-card content for {category}/{material_id}")
    description, fun_fact, examples = content[language]
    return {
        "description": description,
        "fun_fact": fun_fact,
        "examples": examples,
    }


def get_collection_flip_copy(category: str, material_id: str) -> dict:
    """Return bilingual, concise copy for one stable material collection card ID."""
    language = init_language()
    content = COLLECTION_FLIP_COPY.get(category, {}).get(material_id)
    if not content:
        raise KeyError(f"No collection flip-card content for {category}/{material_id}")
    description, fun_fact, examples = content[language]
    return {
        "description": description,
        "fun_fact": fun_fact,
        "examples": examples,
    }


def localize_material_card(card: dict) -> dict:
    if init_language() == "id":
        return card
    localized = dict(card)
    class_name = str(card.get("class_name", "")).strip()
    class_name_en = {
        "Kelas: Mamalia": "Class: Mammals",
        "Kelas: Aves": "Class: Birds",
        "Kelas: Reptilia": "Class: Reptiles",
        "Kelas: Amfibia": "Class: Amphibians",
        "Kelas: Pisces": "Class: Fish",
        "Kelas: Invertebrata": "Class: Invertebrates",
        "Klasifikasi Dasar": "Basic Classification",
        "Morfologi Akar": "Root Morphology",
        "Morfologi Daun": "Leaf Morphology",
        "Anatomi Batang": "Stem Anatomy",
        "Organ Reproduksi": "Reproductive Organ",
    }.get(class_name)
    if class_name_en:
        localized["class_name"] = class_name_en
    title = str(card.get("title", ""))
    if title in MATERIAL_EN:
        en_title, en_description, en_characteristics = MATERIAL_EN[title]
        localized["title"] = en_title
        localized["description"] = en_description
        localized["characteristics"] = en_characteristics
        localized["class_name"] = localized.get("class_name", "")
    return localized


def localize_quiz_question(question: dict) -> dict:
    localized = dict(question)
    if isinstance(question.get("question"), dict):
        language = init_language()
        localized["question"] = question["question"][language]
        localized["explanation"] = question["explanation"][language]
        localized["options"] = {
            option_id: localized_text[language]
            for option_id, localized_text in question["options"].items()
        }
        return localized
    if init_language() == "id":
        return question
    text = str(question.get("question", ""))
    replacements = {
        "Kelompok hewan": "Which animal group",
        "Manakah di antara hewan berikut": "Which of the following animals",
        "Ciri khas": "The characteristic",
        "Amfibia seperti katak": "An amphibian such as a frog",
        "Kelompok hewan yang tidak memiliki tulang belakang": "The animal group that does not have a backbone",
        "Hewan yang memakan tumbuhan": "An animal that eats plants",
        "Hewan pemakan daging": "A meat-eating animal",
        "Hewan yang mengonsumsi baik tumbuhan maupun daging": "An animal that eats both plants and other animals",
        "Kaki berselaput": "Webbed feet",
        "Satwa yang sebagian besar": "An animal that mostly",
        "Gas yang diserap tumbuhan": "The gas absorbed by plants during photosynthesis",
        "Berapa": "How many",
        "Berapakah": "How many",
    }
    for indonesian, english in replacements.items():
        if indonesian in text:
            text = text.replace(indonesian, english)
    localized["question"] = text
    option_translation = {
        "Mamalia": "Mammals",
        "Aves": "Aves",
        "Reptilia": "Reptiles",
        "Amfibia": "Amphibians",
        "Invertebrata": "Invertebrates",
        "Herbivora": "Herbivores",
        "Karnivora": "Carnivores",
        "Omnivora": "Omnivores",
        "Arboreal": "Arboreal",
        "Berenang": "Swimming",
        "Akar tunggang": "Taproot",
        "Akar serabut": "Fibrous root",
        "Monokotil": "Monocot",
        "Dikotil": "Dicot",
        "Kambium": "Cambium",
        "Karbon Dioksida (CO2)": "Carbon Dioxide (CO2)",
        "Oksigen (O2)": "Oxygen (O2)",
    }
    localized["options"] = [
        option_translation.get(str(option), str(option)) for option in question.get("options", [])
    ]
    if str(question.get("correct_answer", "")) in option_translation:
        localized["correct_answer"] = option_translation[str(question["correct_answer"])]
    localized["explanation"] = "English quiz feedback follows the same verified answer and concept."
    return localized


def render_language_switcher(compact: bool = True):
    init_language()
    current = st.session_state["language"]
    widget_key = (
        f"biova_language_control_"
        f"{int(st.session_state.get('_language_widget_revision', 0))}"
    )
    selected = st.segmented_control(
        "Language",
        options=("ID", "EN"),
        default="ID" if current == "id" else "EN",
        key=widget_key,
        label_visibility="collapsed",
    )
    selected_language = {"ID": "id", "EN": "en"}.get(selected)
    if selected_language and selected_language != current:
        set_language(selected_language)
        st.rerun()
