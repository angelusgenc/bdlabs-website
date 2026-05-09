export default function BDLabsLandingPage() {
  return (
    <div className="min-h-screen bg-[#f6f8ff] text-[#111827] overflow-x-hidden">
      {/* NAVBAR */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-white/40">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-violet-600 to-blue-500 flex items-center justify-center shadow-lg shadow-violet-500/20">
              <span className="text-white text-xl font-black">✦</span>
            </div>

            <div>
              <div className="text-2xl font-black tracking-tight">
                BD <span className="text-violet-600">Labs</span>
              </div>
              <div className="text-xs text-slate-500 tracking-wide">
                AI Systems
              </div>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
            <a href="#features" className="hover:text-violet-600 transition">Özellikler</a>
            <a href="#how" className="hover:text-violet-600 transition">Nasıl Çalışır?</a>
            <a href="#products" className="hover:text-violet-600 transition">Ürünler</a>
            <a href="#contact" className="hover:text-violet-600 transition">İletişim</a>
          </nav>

          <button className="px-5 py-3 rounded-2xl bg-gradient-to-r from-violet-600 to-blue-500 text-white font-semibold shadow-xl shadow-violet-500/20 hover:scale-105 transition-all duration-300">
            Ücretsiz Demo
          </button>
        </div>
      </header>

      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-violet-300/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-blue-300/30 rounded-full blur-3xl"></div>

        <div className="max-w-7xl mx-auto px-6 pt-24 pb-28 relative z-10 grid lg:grid-cols-2 gap-20 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-violet-100 text-violet-700 font-semibold text-sm mb-8">
              ✨ Yapay Zekâ Destekli Sesli Randevu Sistemi
            </div>

            <h1 className="text-6xl lg:text-7xl font-black leading-[0.95] tracking-tight text-slate-900">
              Telefonunuz artık
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-blue-500">
                kendi kendine
              </span>
              randevu alıyor.
            </h1>

            <p className="mt-8 text-xl leading-9 text-slate-600 max-w-xl">
              Ece AI müşterilerinizi doğal Türkçeyle karşılar.
              Telefonları cevaplar.
              Randevu oluşturur.
              WhatsApp bildirimi gönderir.
              Siz sadece işinize odaklanırsınız.
            </p>

            <div className="flex flex-wrap gap-4 mt-10">
              <button className="px-8 py-5 rounded-3xl bg-gradient-to-r from-violet-600 to-blue-500 text-white text-lg font-bold shadow-2xl shadow-violet-500/20 hover:scale-105 transition-all duration-300">
                Ücretsiz Demo Başlat
              </button>

              <button className="px-8 py-5 rounded-3xl bg-white border border-slate-200 text-slate-700 text-lg font-semibold hover:border-violet-300 hover:text-violet-600 transition-all duration-300 shadow-lg">
                ▶ Nasıl Çalıştığını İzle
              </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-5 mt-16">
              {[
                ['7/24', 'Kesintisiz Hizmet'],
                ['30 sn', 'Kurulum'],
                ['∞', 'Eş Zamanlı Görüşme'],
                ['₺499', 'Başlangıç Fiyatı'],
              ].map((item, i) => (
                <div key={i} className="bg-white/80 backdrop-blur-xl border border-white/50 rounded-3xl p-5 shadow-xl shadow-slate-200/50">
                  <div className="text-3xl font-black text-violet-600">
                    {item[0]}
                  </div>
                  <div className="text-sm text-slate-500 mt-2 leading-6">
                    {item[1]}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* HERO VISUAL */}
          <div className="relative">
            <div className="absolute -top-10 -right-10 w-48 h-48 bg-violet-400/20 rounded-full blur-3xl"></div>

            <div className="relative bg-white/70 backdrop-blur-2xl rounded-[40px] border border-white/60 shadow-[0_40px_120px_rgba(15,23,42,0.12)] p-6">
              <img
                src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=1200&auto=format&fit=crop"
                alt="Call Center"
                className="rounded-[30px] h-[620px] object-cover w-full"
              />

              <div className="absolute top-10 left-10 bg-white rounded-3xl shadow-2xl p-5 w-72 backdrop-blur-xl border border-slate-100 animate-pulse">
                <div className="text-sm font-bold text-slate-900">
                  Gelen Çağrı
                </div>

                <div className="mt-3 flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-violet-600 to-blue-500"></div>

                  <div>
                    <div className="font-semibold">Ece AI Aktif</div>
                    <div className="text-sm text-green-500">Müşteriyle konuşuyor...</div>
                  </div>
                </div>

                <div className="mt-4 flex gap-1 items-center">
                  {[12, 24, 18, 34, 20, 40, 16, 28].map((h, i) => (
                    <div
                      key={i}
                      className="w-2 rounded-full bg-violet-500"
                      style={{ height: `${h}px` }}
                    ></div>
                  ))}
                </div>
              </div>

              <div className="absolute bottom-10 right-10 bg-white rounded-3xl shadow-2xl p-5 w-80 border border-slate-100">
                <div className="flex items-center justify-between">
                  <div className="font-bold text-slate-900">
                    WhatsApp Bildirimi
                  </div>
                  <div className="text-xs text-slate-400">Şimdi</div>
                </div>

                <div className="mt-4 text-slate-700 leading-7">
                  Yeni randevu oluşturuldu.<br />
                  <span className="font-bold">Ahmet Yılmaz</span><br />
                  14:30 — Saç Kesimi + Sakal
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how" className="py-28 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="text-violet-600 font-bold uppercase tracking-[0.3em] text-sm">
              Nasıl Çalışır?
            </div>

            <h2 className="text-5xl font-black mt-6 tracking-tight leading-tight">
              Ece AI işletmenize
              <span className="text-violet-600"> 30 saniyede bağlanır.</span>
            </h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mt-20">
            {[
              ['1', 'Telefon Numaranızı Bağlayın', 'Mevcut işletme hattınızı kullanmaya devam edin.'],
              ['2', 'Ece Çağrıları Karşılasın', 'Doğal Türkçeyle müşterilerinizi karşılar.'],
              ['3', 'Randevu Oluşsun', 'Saat, tarih ve müşteri bilgileri kaydedilir.'],
              ['4', 'Bildirim Size Gelsin', 'WhatsApp üzerinden anında haberdar olun.'],
            ].map((item, i) => (
              <div
                key={i}
                className="group bg-gradient-to-b from-[#f8f9ff] to-white border border-slate-100 rounded-[32px] p-8 shadow-xl shadow-slate-100 hover:-translate-y-2 transition-all duration-300"
              >
                <div className="w-16 h-16 rounded-3xl bg-gradient-to-br from-violet-600 to-blue-500 text-white flex items-center justify-center text-2xl font-black shadow-xl shadow-violet-500/20">
                  {item[0]}
                </div>

                <h3 className="text-2xl font-black mt-8 leading-tight">
                  {item[1]}
                </h3>

                <p className="text-slate-600 leading-8 mt-5 text-lg">
                  {item[2]}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="py-28">
        <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-20 items-center">
          <div>
            <div className="text-violet-600 font-bold uppercase tracking-[0.3em] text-sm">
              Güçlü Özellikler
            </div>

            <h2 className="text-5xl font-black mt-6 tracking-tight leading-tight">
              Müşterileriniz çoğu zaman
              <span className="text-violet-600"> yapay zekâ ile konuştuğunu fark etmez.</span>
            </h2>

            <div className="space-y-6 mt-12">
              {[
                ['🎙', 'Doğal Türkçe konuşma', 'Robot sesi gibi hissettirmez.'],
                ['📅', 'Akıllı takvim sistemi', 'Çakışmaları önler.'],
                ['💬', 'WhatsApp entegrasyonu', 'Anlık bildirimler gönderir.'],
                ['📱', 'Tablet yönetimi', 'Takviminizi tek ekranda yönetin.'],
              ].map((item, i) => (
                <div key={i} className="flex gap-5 bg-white rounded-3xl p-6 shadow-xl shadow-slate-100 border border-slate-100">
                  <div className="w-16 h-16 rounded-3xl bg-violet-100 text-3xl flex items-center justify-center">
                    {item[0]}
                  </div>

                  <div>
                    <div className="text-2xl font-black">
                      {item[1]}
                    </div>

                    <div className="text-slate-600 mt-2 text-lg leading-8">
                      {item[2]}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="bg-gradient-to-br from-violet-600 to-blue-500 rounded-[40px] p-10 text-white shadow-[0_40px_120px_rgba(99,102,241,0.35)]">
              <div className="text-sm uppercase tracking-[0.3em] opacity-70">
                Canlı Dashboard
              </div>

              <div className="mt-10 space-y-6">
                {[1,2,3].map((i) => (
                  <div key={i} className="bg-white/10 backdrop-blur-xl rounded-3xl p-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-bold text-lg">Yeni Randevu</div>
                        <div className="text-white/70 mt-1">Müşteri: Mehmet Kaya</div>
                      </div>

                      <div className="text-green-300 font-bold">
                        Onaylandı
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* PRODUCTS */}
      <section id="products" className="py-28 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="text-violet-600 font-bold uppercase tracking-[0.3em] text-sm">
              Ece AI Ekosistemi
            </div>

            <h2 className="text-5xl font-black mt-6 tracking-tight leading-tight">
              Yapay zekânın yeni nesli.
            </h2>
          </div>

          <div className="grid lg:grid-cols-4 gap-8 mt-20">
            <div className="rounded-[36px] bg-gradient-to-br from-violet-600 to-blue-500 p-[1px] shadow-[0_30px_80px_rgba(99,102,241,0.3)]">
              <div className="bg-[#0f172a] rounded-[36px] p-8 h-full text-white">
                <div className="inline-flex px-4 py-2 rounded-full bg-green-500/20 text-green-300 text-sm font-bold">
                  Aktif Sistem
                </div>

                <h3 className="text-3xl font-black mt-8 leading-tight">
                  Ece AI Appointment
                </h3>

                <p className="mt-6 text-slate-300 leading-8 text-lg">
                  Telefonları cevaplayan ve otomatik randevu oluşturan AI sistemi.
                </p>

                <button className="mt-10 w-full py-4 rounded-2xl bg-gradient-to-r from-violet-600 to-blue-500 font-bold text-lg">
                  Şimdi Başla
                </button>
              </div>
            </div>

            {[
              ['Ece AI Personal', 'Kişisel AI asistanınız.'],
              ['Ece AI Teams', 'Ekipler için ortak AI hafızası.'],
              ['Ece AI Health', 'Klinikler için AI operasyon sistemi.'],
            ].map((item, i) => (
              <div key={i} className="relative bg-[#f8f9ff] border border-slate-200 rounded-[36px] p-8 opacity-70 overflow-hidden">
                <div className="absolute top-5 right-5 px-4 py-2 rounded-full bg-slate-200 text-slate-600 text-xs font-bold uppercase tracking-wide">
                  Yakında
                </div>

                <h3 className="text-3xl font-black mt-8 leading-tight text-slate-800">
                  {item[0]}
                </h3>

                <p className="mt-6 text-slate-500 leading-8 text-lg">
                  {item[1]}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="relative py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-violet-600 to-blue-500"></div>

        <div className="absolute top-0 left-0 w-full h-full opacity-10">
          <div className="absolute top-20 left-20 w-80 h-80 rounded-full border border-white"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 rounded-full border border-white"></div>
        </div>

        <div className="max-w-5xl mx-auto px-6 relative z-10 text-center text-white">
          <div className="text-sm uppercase tracking-[0.4em] font-bold opacity-80">
            Ece AI
          </div>

          <h2 className="text-6xl font-black mt-8 leading-tight tracking-tight">
            Bir müşteriyi daha kaçırmayın.
          </h2>

          <p className="text-2xl leading-10 mt-8 opacity-90 max-w-3xl mx-auto">
            Ece AI bugün işletmeniz için çalışmaya başlasın.
            Telefonlarınızı otomatik cevaplasın.
            Randevularınızı yönetsin.
          </p>

          <button className="mt-12 px-10 py-6 rounded-3xl bg-white text-violet-700 text-xl font-black shadow-2xl hover:scale-105 transition-all duration-300">
            Ücretsiz Demo Talep Et
          </button>
        </div>
      </section>

      {/* FOOTER */}
      <footer id="contact" className="bg-[#0f172a] text-white py-20">
        <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-3 gap-16">
          <div>
            <div className="text-4xl font-black tracking-tight">
              BD <span className="text-violet-400">Labs</span>
            </div>

            <p className="mt-6 text-slate-400 leading-8 text-lg max-w-md">
              Yeni nesil yapay zekâ sistemleri geliştiriyoruz.
              Sesli AI, otomasyon ve gerçek dünya çözümleri.
            </p>
          </div>

          <div>
            <div className="text-xl font-black mb-6">
              Menü
            </div>

            <div className="space-y-4 text-slate-400 text-lg">
              <div>Ana Sayfa</div>
              <div>Özellikler</div>
              <div>Ürünler</div>
              <div>Demo</div>
              <div>İletişim</div>
            </div>
          </div>

          <div>
            <div className="text-xl font-black mb-6">
              İletişim
            </div>

            <div className="space-y-4 text-slate-400 text-lg leading-8">
              <div>info@bdlabs.com.tr</div>
              <div>İstanbul / Türkiye</div>
              <div>WhatsApp Destek</div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
