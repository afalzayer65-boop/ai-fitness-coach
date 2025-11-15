from flask import Flask, render_template_string, request
from openai import OpenAI
import os   # needed for environment variable

# Read the key from Render environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# PayPal links
PAYPAL_STARTER = "https://paypal.me/3lissw/9"
PAYPAL_TRANSFORM = "https://paypal.me/3lissw/29"
PAYPAL_VIP = "https://paypal.me/3lissw/79"

<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>AI Fitness Coach – Custom Plans & Bundles</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Poppins", sans-serif;
      background: radial-gradient(circle at top, #0f172a, #020617);
      color: #e5e7eb;
    }
    a { color: inherit; text-decoration: none; }

    .wrapper {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      padding: 24px 16px 16px;
      text-align: center;
    }
    .nav-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,0.4);
      font-size: 11px;
      color: #9ca3af;
    }
    .logo {
      width: 80px;
      height: 80px;
      border-radius: 24px;
      background: conic-gradient(from 160deg, #22c55e, #0ea5e9, #4f46e5, #22c55e);
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 14px auto 6px;
      font-size: 34px;
      box-shadow: 0 12px 40px rgba(15,23,42,0.85);
    }
    header h1 {
      margin: 4px 0;
      font-size: 2.4rem;
    }
    header p {
      margin: 0;
      opacity: 0.9;
      max-width: 540px;
      margin-inline: auto;
      font-size: 0.95rem;
    }

    main {
      max-width: 1120px;
      width: 100%;
      margin: 0 auto 40px;
      padding: 0 16px 40px;
      flex: 1;
    }

    .pill-row {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 8px;
      margin-top: 10px;
      font-size: 11px;
      color: #9ca3af;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: minmax(0, 3fr) minmax(0, 2.2fr);
      gap: 20px;
      margin-top: 26px;
    }
    @media (max-width: 900px) {
      .hero-grid {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .card {
      background: #020617;
      border-radius: 20px;
      padding: 22px;
      border: 1px solid rgba(148, 163, 184, 0.45);
      box-shadow: 0 18px 50px rgba(15,23,42,0.9);
      position: relative;
      overflow: hidden;
    }

    .tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      font-size: 11px;
      border-radius: 999px;
      border: 1px solid rgba(34,197,94,0.5);
      background: rgba(22,163,74,0.16);
      color: #bbf7d0;
    }

    h2.section-title {
      font-size: 1.4rem;
      margin: 0 0 10px;
    }

    /* FORM STYLING */
    form label {
      font-weight: 500;
      font-size: 0.85rem;
    }
    textarea,
    input[type="text"],
    input[type="number"] {
      width: 100%;
      margin-top: 4px;
      margin-bottom: 10px;
      border-radius: 12px;
      border: 1px solid #475569;
      background: #020617;
      padding: 8px 10px;
      color: #e5e7eb;
      font-size: 13px;
    }
    textarea {
      min-height: 80px;
      resize: vertical;
    }
    textarea:focus,
    input:focus {
      outline: none;
      border-color: #22c55e;
      box-shadow: 0 0 0 1px rgba(34,197,94,0.5);
    }

    .field-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    @media (max-width: 600px) {
      .field-row {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .goal-chip-row {
      margin-top: 6px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .goal-chip {
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid rgba(34,197,94,0.4);
      background: rgba(22,163,74,0.12);
      font-size: 11px;
      cursor: pointer;
    }
    .goal-chip:hover {
      background: rgba(34,197,94,0.25);
    }

    .primary-btn {
      margin-top: 8px;
      padding: 9px 20px;
      border-radius: 999px;
      border: none;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      background: linear-gradient(135deg, #22c55e, #16a34a);
      color: #f9fafb;
      box-shadow: 0 12px 30px rgba(34,197,94,0.55);
      transition: transform 0.06s, box-shadow 0.06s, opacity 0.06s;
    }
    .primary-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 16px 34px rgba(34,197,94,0.7);
    }
    .primary-btn:disabled {
      opacity: 0.65;
      cursor: wait;
    }

    .hint {
      font-size: 11px;
      color: #9ca3af;
    }

    .loading {
      display: none;
      margin-top: 8px;
      font-size: 12px;
      color: #a5b4fc;
    }

    /* PLAN DISPLAY */
    .plan-card {
      border-radius: 18px;
      padding: 16px 16px 18px;
      background: #020617;
      border: 1px solid rgba(148,163,184,0.6);
      font-size: 14px;
      line-height: 1.6;
      max-height: 520px;
      overflow-y: auto;
    }
    .plan-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    .badge {
      font-size: 11px;
      padding: 4px 9px;
      border-radius: 999px;
      border: 1px solid rgba(56,189,248,0.5);
      background: rgba(8,47,73,0.7);
      color: #bae6fd;
    }
    .plan-card h3, .plan-card h4 {
      color: #a5b4fc;
    }

    /* HOW IT WORKS */
    .steps {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 10px;
      font-size: 13px;
    }
    @media (max-width: 900px) {
      .steps {
        grid-template-columns: minmax(0, 1fr);
      }
    }
    .step {
      background: #020617;
      border-radius: 16px;
      padding: 14px;
      border: 1px solid rgba(51,65,85,0.8);
    }
    .step-num {
      width: 22px;
      height: 22px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: rgba(37,99,235,0.25);
      font-size: 12px;
      margin-bottom: 4px;
    }

    /* PRICING */
    .pricing-section {
      margin-top: 30px;
    }
    .pricing-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
      margin-top: 12px;
    }
    @media (max-width: 900px) {
      .pricing-grid {
        grid-template-columns: minmax(0, 1fr);
      }
    }
    .price-card {
      background: #020617;
      border-radius: 18px;
      padding: 18px;
      border: 1px solid rgba(148,163,184,0.45);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .price-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .price-name {
      font-size: 1.1rem;
      font-weight: 600;
    }
    .price-tag {
      font-size: 1.5rem;
    }
    .price-tag span {
      font-size: 0.8rem;
      color: #9ca3af;
    }
    .price-list {
      font-size: 0.86rem;
      color: #d1d5db;
      padding-left: 18px;
      margin: 8px 0 0;
    }
    .pill-popular {
      font-size: 10px;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid rgba(249,115,22,0.7);
      background: rgba(251,146,60,0.18);
      color: #fed7aa;
    }
    .price-cta {
      margin-top: 12px;
      padding: 8px 14px;
      border-radius: 999px;
      border: none;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      background: linear-gradient(135deg, #3b82f6, #2563eb);
      color: #f9fafb;
      text-align: center;
      text-decoration: none;
      display: inline-block;
    }
    .price-cta:hover {
      filter: brightness(1.06);
    }

    /* TESTIMONIALS */
    .testimonials {
      margin-top: 30px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      font-size: 0.85rem;
    }
    @media (max-width: 900px) {
      .testimonials {
        grid-template-columns: minmax(0, 1fr);
      }
    }
    .testimonial {
      background: #020617;
      border-radius: 16px;
      padding: 14px;
      border: 1px solid rgba(51,65,85,0.9);
    }
    .testimonial-name {
      margin-top: 6px;
      font-weight: 500;
      color: #e5e7eb;
    }
    .stars { color: #fbbf24; font-size: 12px; }

    footer {
      text-align: center;
      padding: 12px 0 18px;
      font-size: 11px;
      color: #94a3b8;
    }
  </style>
</head>
<body>
<div class="wrapper">

  <header>
    <div class="nav-pill">⚡ AI-powered fitness plans · Built for your body</div>
    <div class="logo">💪</div>
    <h1>AI Fitness Coach</h1>
    <p>Describe your goal and get a personalized workout + nutrition plan in seconds. Then upsell premium bundles for serious transformations.</p>
    <div class="pill-row">
      <span>Works for home & gym</span>·
      <span>Beginner to advanced</span>·
      <span>No face or voice needed – you’re the owner behind the scenes</span>
    </div>
  </header>
<div style="max-width:1040px;margin:0 auto;">
  <img src="{{ url_for('static', filename='img/hero.png') }}"
       alt="AI Fitness Hero"
       style="width:100%;border-radius:22px;margin:20px 0;box-shadow:0 18px 40px rgba(0,0,0,0.5);">
</div>


  <main>
    <div class="hero-grid">
      <!-- LEFT: FORM -->
      <section class="card">
        <div class="tag">Step 1 · Tell the AI about your body & goal</div>
        <h2 class="section-title" style="margin-top:10px;">Create your custom plan</h2>

        <form id="plan-form" method="POST">
          <label for="goal">Main goal</label>
          <textarea id="goal" name="goal" placeholder="Example: I want to lose 8kg in 3 months, train 4x per week at the gym, and keep some muscle.">{{ goal }}</textarea>

          <div class="goal-chip-row">
            <div class="goal-chip" onclick="quickGoal('Lose body fat and keep muscle, 4 sessions per week, mostly machines + treadmill.')">Lose fat 🫠</div>
            <div class="goal-chip" onclick="quickGoal('Build muscle and strength, 5 gym sessions per week, focus on chest, back and legs.')">Build muscle 💪</div>
            <div class="goal-chip" onclick="quickGoal('Improve conditioning, run 5 km without stopping, 3 cardio days + 2 strength days.')">Endurance 🏃‍♂️</div>
            <div class="goal-chip" onclick="quickGoal('Total beginner, no equipment, I want a simple 3-day full body routine at home.')">Beginner 🐣</div>
          </div>

          <div class="field-row" style="margin-top:10px;">
            <div>
              <label for="age">Age (optional)</label>
              <input id="age" name="age" type="number" min="10" max="80" placeholder="14" />
            </div>
            <div>
              <label for="gender">Gender (optional)</label>
              <input id="gender" name="gender" type="text" placeholder="Male / Female / Other" />
            </div>
          </div>

          <div class="field-row">
            <div>
              <label for="weight">Current weight</label>
              <input id="weight" name="weight" type="text" placeholder="e.g. 72 kg" />
            </div>
            <div>
              <label for="goal_weight">Goal weight</label>
              <input id="goal_weight" name="goal_weight" type="text" placeholder="e.g. 64 kg" />
            </div>
          </div>

          <div class="field-row">
            <div>
              <label for="experience">Training level</label>
              <input id="experience" name="experience" type="text" placeholder="Beginner / Intermediate / Advanced" />
            </div>
            <div>
              <label for="medical">Injuries / medical notes</label>
              <input id="medical" name="medical" type="text" placeholder="e.g. knee pain, asthma, none" />
            </div>
          </div>

          <p class="hint">
            The more detail you give (age, gender, weight, experience, injuries), the smarter your plan will be.
          </p>

          <button id="generate-btn" class="primary-btn" type="submit">Generate plan ⚡</button>
          <div id="loading" class="loading">⚙️ Generating your AI plan… this may take a few seconds.</div>
        </form>
      </section>

      <!-- RIGHT: LIVE PLAN -->
      <section class="card">
        <div class="tag">Step 2 · Preview</div>
        <h2 class="section-title" style="margin-top:10px;">Your live plan preview</h2>

        {% if plan %}
          <div class="plan-card">
            <div class="plan-header">
              <h4 style="margin:0;">Your personalized plan</h4>
              <span class="badge">AI generated</span>
            </div>
            <div>
              {{ plan|safe }}
            </div>
          </div>
        {% else %}
          <div class="plan-card" style="display:flex;align-items:center;justify-content:center;text-align:center;">
            <div>
              <h4 style="margin-top:0;">No plan yet</h4>
              <p class="hint">
                Describe your goal on the left and hit <strong>Generate plan</strong>. Your AI coach will build a clear weekly split,
                example workouts, nutrition tips and recovery guidelines.
              </p>
            </div>
          </div>
        {% endif %}
      </section>
    </div>

    <!-- HOW IT WORKS -->
    <section style="margin-top:28px;">
      <div class="tag">Step 3 · Turn this into a business</div>
      <h2 class="section-title" style="margin-top:10px;">How this site works</h2>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <h4 style="margin:4px 0 4px;font-size:0.95rem;">Client fills the form</h4>
          <p>You send them to this page. They type their goal, body stats and limitations. This gives the AI enough info to build a smart program.</p>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <h4 style="margin:4px 0 4px;font-size:0.95rem;">AI builds the plan</h4>
          <p>The AI creates a full training + nutrition plan. You can copy, tweak, export as PDF, or send it via WhatsApp / email.</p>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <h4 style="margin:4px 0 4px;font-size:0.95rem;">They pay for upgrades</h4>
          <p>Use the PayPal buttons below to sell Starter, Transformation bundles, and VIP coaching with monthly support.</p>
        </div>
      </div>
    </section>

    <!-- PRICING / SHOP -->
    <section class="pricing-section">
      <div class="tag">Monetize · Turn your plans into products</div>
      <h2 class="section-title" style="margin-top:10px;">Premium plans & bundles 💸</h2>
      <p class="hint">All payments go directly to your PayPal. You can change prices anytime by editing the amounts in your links.</p>

      <div class="pricing-grid">
        <div class="price-card">
          <div>
            <div class="price-header">
              <div class="price-name">Starter Plan</div>
              <div class="price-tag">$9 <span>one-time</span></div>
            </div>
            <ul class="price-list">
              <li>1 fully custom AI fitness plan</li>
              <li>Workout split + exercises + reps</li>
              <li>Simple nutrition & habit guide</li>
            </ul>
          </div>
          <a class="price-cta" href="{{ paypal_starter }}" target="_blank">Buy Starter via PayPal</a>
        </div>

        <div class="price-card">
          <div>
            <div class="price-header">
              <div class="price-name">Transformation Bundle</div>
              <div class="price-tag">$29 <span>one-time</span></div>
            </div>
            <span class="pill-popular">Most popular</span>
            <ul class="price-list">
              <li>3 phases (8–12 weeks total)</li>
              <li>Updated plan after progress check</li>
              <li>Basic chat support for adjustments</li>
            </ul>
          </div>
          <a class="price-cta" href="{{ paypal_transform }}" target="_blank">Buy Bundle via PayPal</a>
        </div>

        <div class="price-card">
          <div>
            <div class="price-header">
              <div class="price-name">VIP Coaching</div>
              <div class="price-tag">$79 <span>per month</span></div>
            </div>
            <ul class="price-list">
              <li>Everything in Transformation</li>
              <li>Weekly check-ins & adjustments</li>
              <li>Priority WhatsApp / chat support</li>
            </ul>
          </div>
          <a class="price-cta" href="{{ paypal_vip }}" target="_blank">Join VIP via PayPal</a>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS -->
    <section style="margin-top:30px;">
      <div class="tag">Social proof · Make the page feel trusted</div>
      <h2 class="section-title" style="margin-top:10px;">What clients could say</h2>
      <div class="testimonials">
        <div class="testimonial">
          <div class="stars">★★★★★</div>
          <p>"I dropped almost 6 kg in 5 weeks while keeping my strength. The plan told me exactly what to do each day."</p>
          <div class="testimonial-name">M., 17 – Fat loss</div>
        </div>
        <div class="testimonial">
          <div class="stars">★★★★★</div>
          <p>"The workout split and form tips saved me so much time. I finally have a routine that actually fits my schedule."</p>
          <div class="testimonial-name">A., 19 – Muscle & school balance</div>
        </div>
        <div class="testimonial">
          <div class="stars">★★★★★</div>
          <p>"I just send my stats, pay, and get a full plan in my inbox. Way cheaper than a normal personal trainer."</p>
          <div class="testimonial-name">S., 22 – Busy student</div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    © 2025 AI Fitness Coach. Not medical advice. Always consult a doctor before starting a new training or nutrition plan.
  </footer>
</div>

<script>
  function quickGoal(text) {
    const textarea = document.getElementById('goal');
    textarea.value = text;
    textarea.focus();
  }

  const form = document.getElementById('plan-form');
  const btn = document.getElementById('generate-btn');
  const loading = document.getElementById('loading');

  if (form && btn && loading) {
    form.addEventListener('submit', function () {
      btn.disabled = true;
      btn.innerText = 'Generating...';
      loading.style.display = 'block';
    });
  }
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    plan = None
    goal = ""

    if request.method == "POST":
        goal = request.form.get("goal", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        weight = request.form.get("weight", "").strip()
        goal_weight = request.form.get("goal_weight", "").strip()
        experience = request.form.get("experience", "").strip()
        medical = request.form.get("medical", "").strip()

        if goal:
            context = f"Goal: {goal}\n"
            if age:
                context += f"Age: {age}\n"
            if gender:
                context += f"Gender: {gender}\n"
            if weight:
                context += f"Current weight: {weight}\n"
            if goal_weight:
                context += f"Goal weight: {goal_weight}\n"
            if experience:
                context += f"Training experience: {experience}\n"
            if medical:
                context += f"Medical conditions / injuries: {medical}\n"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.7,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly but professional fitness coach. "
                            "Return ONLY HTML (no <html> or <body> tags). "
                            "Use headings (<h3>, <h4>), paragraphs, and bullet lists. "
                            "Sections: Goal summary, Weekly training split, Example workouts, "
                            "Warm-up & form tips, Nutrition guidelines, Recovery & sleep, Motivation. "
                            "Always keep things safe for teens and beginners."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Create a clear, structured fitness plan for this person:\n{context}",
                    },
                ],
            )
            plan = response.choices[0].message.content

    return render_template_string(
        PAGE,
        plan=plan,
        goal=goal,
        paypal_starter=PAYPAL_STARTER,
        paypal_transform=PAYPAL_TRANSFORM,
        paypal_vip=PAYPAL_VIP,
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)



