# Jobescape Quiz Funnel — full map (quiz_version v7.3.0)

Source: `api.funnel.jobescape.me/constructor/quiz-node/?quiz_title=v7.3.0` · 37 pages · reconstructed 2026-07-24

One branch only: the opening card splits on **used_ai (Yes/No)** into two FOMO cards; everything else is linear. Each answer writes a `funnel_data` variable (shown as `→ writes: x`).

### [0] landing-card_claude (compliant)  ·  _test_
- **branch:** if (used_ai = Yes) → node 9864; if (else) → node 9863
- **Q:** Have you ever used Claude?
- **writes:** cohort_date, used_ai, geo_country_code

### [1] fomo_claude (no)  ·  _test_
- **copy:** You’re right on time — this is where it starts ⏎ Most people begin exactly where you are — with no experience at all. In fact, some of our best students started from zero. The real difference is what you do next ⏎ Continue

### [1] fomo_claude (yes) (compliant)  ·  _test_
- **copy:** You’re ahead – but this is just the start ⏎ Getting started already puts you ahead – but the biggest gap happens next. Some people stay at the surface, others go deeper and unlock what AI can really do ⏎ Continue


## ▸ Section: My Profile

### [2] why_claude  ·  _test_
- **Q:** I want to learn Claude for...
- **options:** Work tasks | Personal use | Growth - I love learning in-demand skills
- **writes:** why_claude, why_claude_label

### [3] status_claude 7  ·  _test_
- **Q:** What’s your current work status?
- **options:** Full-time employee | Freelancer / Self-employed | Business owner | Between jobs / Career switcher | Exploring options
- **writes:** status, status_label

### [4] age 7  ·  _test_
- **Q:** How old are you?
- **options:** 18-24 | 25-34 | 35-44 | 45-54 | 55+
- **writes:** age, age_label

### [5] gender 7  ·  _test_
- **Q:** What's your gender identity?
- **options:** Female | Male | I'd rather skip this one
- **writes:** gender

### [6] goal_claude 7  ·  _test_
- **Q:** How would learning Claude benefit you?
- **options:** Get a promotion or a better job | Work faster | Feel more confident with AI | Start my own business | Earn more
- **writes:** goal, goal_label

### [7] profile_summary (cld)  ·  _test_
- **writes:** used_ai
- **copy:** Did we get everything right? ⏎ Motivation: ⏎ Current status: ⏎ Age: ⏎ Experience with AI: ⏎ Low


## ▸ Section: Challenges

### [8] experience_ai 7  ·  _test_
- **Q:** How would you rate your experience with AI so far?
- **options:** Great – AI already helps me a lot | Good – but I still have a lot to learn | Frustrating – i can’t get it to do what i want | I haven’t really tried yet 
- **writes:** experience_ai

### [9] skills_competitive 7  ·  _test_
- **Q:** Do you feel ready for the way AI is changing career and opportunities?
- **options:** Not really — I need new skills fast | A bit worried — things are changing quickly | Somewhat ready — but I could be behind | Yes - I’m confident in my skills
- **writes:** skills_competitive

### [10] career_scares 7  ·  _test_
- **Q:** What scares you most about AI and your career?
- **options:** Being replaced by someone who uses AI better | Falling behind as others move faster | Losing opportunities without AI on my resume | Nothing - I see AI as an opportunity, not a threat
- **writes:** career_scares

### [11] nothing_worry_teaser (compliant)  ·  _test_
- **copy:** There is nothing to worry about ⏎ The question isn't whether AI will change your career – it already is. The professionals who learn to use it well will have a real advantage – and you can be one of them. ⏎ Karim Lakhani, professor at Harvard Business School: "AI won't replace humans – but humans with AI will replace humans without AI." ⏎ Continue

### [12] often_create 7  ·  _test_
- **Q:** I create documents, reports, or presentations regularly
- **options:** 1 | 2 | 3 | 4 | 5
- **writes:** often_create

### [13] long_fix 6.0.250  ·  _test_
- **Q:** Have you ever used AI to write something and then spent just as long fixing it?
- **options:** Yes, every time - it’s barely faster | Sometimes - it needs a lot of editing | No - AI works well for me | I haven’t tried using AI for writing
- **writes:** long_fix

### [14] polished_documents 7  ·  _test_
- **Q:** What would change if you could get a polished, ready-to-use document in 2 minutes?
- **options:** I’d produce 3x more content | I’d finally stop procrastinating on reports | I’d look way more professional | I’d spend my time on strategy instead of formatting
- **writes:** button-disabled, polished_documents

### [15] stop_fixing_teaser (compliant)  ·  _test_
- **copy:** Create polished content ⏎ . ⏎ Once you learn how to use Claude, it gives you more than drafts. They create polished, formatted, ready-to-use documents – right in the conversation. No copy-pasting. No reformatting. Done. ⏎ Full documents with structure and formatting ⏎ Interactive tables, charts, and dashboards ⏎ Reports with data visualizations

### [16] Idea-app 7  ·  _test_
- **Q:** Have you ever had an idea for an app, website, or tool — but couldn't build it?
- **options:** Yes | No
- **writes:** idea_app

### [17] app_stoppers 7  ·  _test_
- **Q:** What stopped you?
- **options:** I don’t know how to code and thought I had to | Hiring a developer is too expensive | I started but gave up – too many technical problems | I didn’t know where to begin
- **writes:** button-disabled, app_stoppers

### [18] app_without 7  ·  _test_
- **Q:** Do you believe it's possible to build a real working app without coding experience?
- **options:** No, that seems unlikely | Maybe with AI, but I’m skeptical | Yes – I’ve seen people do it
- **writes:** app_without

### [19] build_easy_teaser (compliant)  ·  _test_
- **copy:** Building an app has never been this easy. ⏎ Need a tracker? A dashboard? A client tool? A portfolio site? Just tell Claude what you want. Often in minutes, it's built, tested, and ready to use. No code. No developer. No expensive invoices. Just you and Claude. ⏎ Describe your idea in normal language ⏎ Claude builds, tests, and debugs the entire thing ⏎ Websites, tools, automations, dashboards, apps ⏎ No coding experience required – zero


## ▸ Section: Personalization

### [20] prefer_learn  ·  _test_
- **Q:** How do you prefer to learn?
- **options:** At my own pace | With set deadlines
- **writes:** prefer_learn

### [21] time_goal 7  ·  _test_
- **Q:** How much time you want to dedicate to achieve your goal?
- **options:** 10 min/day | 20 min/day | 30 min/day |  1 hour/day
- **writes:** time_goal, time_goal_label

### [22] approach_best  ·  _test_
- **Q:** What approach works best for you?
- **options:** 80% theory + 20% practice | 80% practice + 20% theory
- **writes:** approach_best

### [23] portfolio_prefer  ·  _test_
- **Q:** Would you like to include your projects to a portfolio site we built for you?
- **options:** Yes | No
- **writes:** coding_experience

### [24] ai_mentor_prefer  ·  _test_
- **Q:** Would you like an AI mentor to guide you as you learn?
- **options:** Yes | No
- **writes:** ai_mentor_prefer

### [25] simple_plan_teaser 7  ·  _test_
- **copy:** Your guided step-by-step plan is almost ready! ⏎ Continue

### [26] certification_advantage (compliant)  ·  _test_
- **Q:** Would an official AI certification give you an advantage in your career?
- **options:** Definitely - it would set me apart | Probably - it’s a growing field | I don’t think certifications matter for me
- **writes:** certification_advantage

### [27] certificate_teaser_claude (compliant)  ·  _test_
- **copy:** Get your Claude skills certificate from Jobescape ⏎ Don't just learn AI – show it. Complete the Jobescape course, finish the final assessment, and add a certificate of completion to your resume and LinkedIn – proof of the practical AI skills you built. ⏎ Certificate of completion from Jobescape ⏎ A certificate you can add to your resume and LinkedIn ⏎ Focused on real, practical AI skills – not just theory ⏎ Bite-sized lessons – about 15 minutes a day

### [28] stopped_before_claude  ·  _test_
- **Q:** What kept you from advancing with Claude before?
- **options:** I don’t have the right plan or guidance | I’m afraid I’ll waste time and see no results | I’m too busy to focus on learning something new | It all seems too new and confusing
- **writes:** stopped_before_label, stopped_before

### [29] loader_claude (compliant)  ·  _test_
- **writes:** first-node-finished, first-loader-stopped, second-node-finished, second-loader-stopped, third-node-finished, third-loader-stopped
- **copy:** Setting Goals ⏎ Goals ⏎ Growth Areas ⏎ Setting Growth Areas ⏎ Content ⏎ Picking content

### [30] ai_profile_teaser_claude (compliant)  ·  _test_
- **writes:** experience_ai
- **copy:** Here's your AI profile ⏎ Based on your answers, we've created your personal AI readiness assessment. ⏎ Advanced ⏎ Good, but not great ⏎ Low ⏎ No experience

### [31] email_universal (compliant)  ·  _test_
- **writes:** geo_country_code, email_error, gender, user_gender, fb_timestamp, pending, pixel_event_id, email_consent, email
- **copy:** We respect your privacy and we are committed to protecting your personal data. Your data will be processed in accordance with our ⏎ Continue

### [32] name_default  ·  _test_
- **writes:** name, pending
- **copy:** Continue

### [33] personal_plan_teaser_claude (compliant)  ·  _test_
- **copy:** Your Personal Plan to Learn Claude ⏎ Build the AI skills that can boost your work pace and efficiency! ⏎ A guided course to get confident using Claude ⏎ 6-module guided course ⏎ Chat for real work – delegate real tasks to Claude and ship your first working tool ⏎ Design your workspace – build a Claude project that remembers your standards and files

### [34] sp cld v2 (compliant)  ·  _selling-page_
- **writes:** timer_timeouted, paywall_trigger_visible, apple_pay_session, device_type, inline_error, decline_message, payment_form, decline, error_message, stopped_before, geo_country_code
- **copy:** Start with ⏎ % off ⏎ Start Learning ⏎ Claude ⏎ today ⏎ with

### [35] sp cld v2 (compliant) chase  ·  _selling-page_
- **writes:** timer_timeouted, paywall_trigger_visible, apple_pay_session, device_type, inline_error, decline_message, payment_form, decline, error_message, stopped_before, geo_country_code
- **copy:** Start with ⏎ % off ⏎ Start Learning ⏎ Claude ⏎ today ⏎ with
