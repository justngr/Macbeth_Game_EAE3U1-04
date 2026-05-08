import random
import sys
import pygame

WIDTH, HEIGHT = 1100, 700
FPS = 60
PLAYER_SPEED = 4
RAPID_TIME_SECONDS = 30

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
BG = (20, 23, 30)
PLAYER_COLOR = (90, 180, 255)
ZONE_COLOR = (102, 205, 149)
ZONE_HOVER = (255, 210, 90)
ZONE_DONE = (120, 130, 145)
PANEL = (48, 52, 63)
PANEL_DARK = (32, 36, 46)
GOOD = (70, 190, 110)
BAD = (210, 90, 90)
ACCENT = (188, 152, 88)

RAPID_QUIZ = [
    {"q": "Who gives Macbeth the first prophecy?", "choices": ["Macduff", "The Witches", "Duncan", "Banquo"], "answer": 1},
    {"q": "Who is murdered in Act 2?", "choices": ["Banquo", "Malcolm", "King Duncan", "Macduff"], "answer": 2},
    {"q": "Who sees Banquo's ghost?", "choices": ["Lady Macbeth", "Macbeth", "Macduff", "Ross"], "answer": 1},
    {"q": "What forest appears to move toward Dunsinane?", "choices": ["Sherwood", "Birnam Wood", "Arden", "Caledon"], "answer": 1},
    {"q": "Who says 'Out, damned spot!'?", "choices": ["Lady Macbeth", "Witch 1", "Hecate", "Lady Macduff"], "answer": 0},
    {"q": "Who kills Macbeth?", "choices": ["Malcolm", "Banquo", "Macduff", "Siward"], "answer": 2},
    {"q": "Who becomes king at the end?", "choices": ["Macduff", "Malcolm", "Fleance", "Donalbain"], "answer": 1},
    {"q": "What title is Macbeth given early on?", "choices": ["Thane of Cawdor", "Duke of York", "Prince of Wales", "Earl of Fife"], "answer": 0},
]

ACTS = [
    {"name": "Act 1", "rect": pygame.Rect(70, 190, 190, 100), "scenes": [
        {"title": "Scene 1 - The Witches on the Heath", "script": ["Witch 1: When shall we three meet again?", "Witch 2: When the battle's lost and won.", "Witch 3: That will be ere the set of sun.", "All Witches: Fair is foul, and foul is fair."], "questions": [("The witches appear before Macbeth is seen.", True), ("The witches promise peace and calm weather.", False)]},
        {"title": "Scene 2 - Report from Battle", "script": ["Captain: Brave Macbeth has won the field.", "Duncan: O valiant cousin!", "Ross: The thane of Cawdor has betrayed us.", "Duncan: What he hath lost, noble Macbeth hath won."], "questions": [("Macbeth is rewarded with Cawdor's title.", True), ("Duncan punishes Macbeth in this scene.", False)]},
        {"title": "Scene 3 - Prophecies Given", "script": ["Witch: All hail, Macbeth, that shalt be king hereafter!", "Banquo: What of me?", "Witch: Thou shalt get kings, though thou be none.", "Macbeth: Stay, you imperfect speakers."], "questions": [("The witches predict Banquo's heirs will be kings.", True), ("Macbeth ignores the witches immediately.", False)]},
        {"title": "Scene 4 - Prince of Cumberland", "script": ["Duncan: We name Malcolm Prince of Cumberland.", "Macbeth: That is a step on which I must fall down or else o'erleap.", "Macbeth: Stars, hide your fires.", "Banquo: New honors come upon him."], "questions": [("Malcolm is named Prince of Cumberland.", True), ("Macbeth tells Duncan about his dark desire.", False)]},
        {"title": "Scene 5 - Lady Macbeth Reads", "script": ["Lady Macbeth: Thy nature is too full of the milk of human kindness.", "Lady Macbeth: Come, you spirits, unsex me here.", "Messenger: The king comes here tonight.", "Lady Macbeth: Leave all the rest to me."], "questions": [("Lady Macbeth calls on spirits to harden her.", True), ("Lady Macbeth advises Macbeth to stay passive.", False)]},
        {"title": "Scene 6 - Duncan at Inverness", "script": ["Duncan: This castle hath a pleasant seat.", "Banquo: The air is delicate.", "Lady Macbeth: All our service in every point twice done and then done double.", "Duncan: Fair and noble hostess."], "questions": [("Duncan feels welcomed and safe here.", True), ("Banquo warns Duncan to flee at once.", False)]},
        {"title": "Scene 7 - Macbeth Decides", "script": ["Macbeth: We will proceed no further in this business.", "Lady Macbeth: When you durst do it, then you were a man.", "Macbeth: I am settled.", "Lady Macbeth: False face must hide what the false heart doth know."], "questions": [("Lady Macbeth persuades Macbeth to continue the plan.", True), ("Macbeth tells everyone the murder plan.", False)]},
    ]},
    {"name": "Act 2", "rect": pygame.Rect(280, 190, 190, 100), "scenes": [
        {"title": "Scene 1 - Dagger Soliloquy", "script": ["Banquo: I dreamt of the weird sisters.", "Macbeth: Is this a dagger I see before me?", "Macbeth: Thou marshall'st me the way that I was going.", "Bell: A bell rings."], "questions": [("Macbeth hallucinates a dagger.", True), ("Banquo tells Macbeth to murder Duncan.", False)]},
        {"title": "Scene 2 - Duncan Murdered", "script": ["Lady Macbeth: That which hath made them drunk hath made me bold.", "Macbeth: I have done the deed.", "Macbeth: Sleep no more!", "Lady Macbeth: A little water clears us of this deed."], "questions": [("Macbeth hears imaginary voices after the murder.", True), ("Lady Macbeth wants to confess immediately.", False)]},
        {"title": "Scene 3 - Discovery", "script": ["Porter: Knock, knock!", "Macduff: O horror, horror, horror!", "Macbeth: Had I but died an hour before this chance...", "Donalbain: There's daggers in men's smiles."], "questions": [("Macduff discovers Duncan's body.", True), ("Duncan's sons remain safely in Scotland.", False)]},
        {"title": "Scene 4 - Unnatural Signs", "script": ["Old Man: 'Tis day, and yet dark night strangles the lamp.", "Ross: Duncan's horses turned wild.", "Macduff: Those that Macbeth hath slain.", "Ross: Nature is troubled."], "questions": [("Nature behaves strangely after Duncan's death.", True), ("Everything returns to normal immediately.", False)]},
    ]},
    {"name": "Act 3", "rect": pygame.Rect(490, 190, 190, 100), "scenes": [
        {"title": "Scene 1 - Banquo Suspects", "script": ["Banquo: Thou hast it now: king, Cawdor, Glamis.", "Macbeth: Our fears in Banquo stick deep.", "Macbeth: It is concluded.", "Murderers: We are resolved."], "questions": [("Macbeth arranges Banquo's murder.", True), ("Banquo fully trusts Macbeth.", False)]},
        {"title": "Scene 2 - Macbeth's Fear", "script": ["Lady Macbeth: Naught's had, all's spent.", "Macbeth: Full of scorpions is my mind.", "Macbeth: Things bad begun make strong themselves by ill.", "Lady Macbeth: You must leave this."], "questions": [("Macbeth says his mind is tormented.", True), ("Macbeth feels calm and safe here.", False)]},
        {"title": "Scene 3 - Ambush", "script": ["Murderer: Stand to't.", "Banquo: Fly, good Fleance!", "Murderer: Who did strike out the light?", "Murderer: Fleance is escaped."], "questions": [("Fleance escapes the ambush.", True), ("Banquo survives this scene.", False)]},
        {"title": "Scene 4 - Banquet Ghost", "script": ["Macbeth: The table's full.", "Macbeth: Never shake thy gory locks at me.", "Lady Macbeth: Are you a man?", "Lords: The king is troubled."], "questions": [("Macbeth sees Banquo's ghost.", True), ("All guests can see the ghost too.", False)]},
        {"title": "Scene 5 - Hecate", "script": ["Hecate: How did you dare trade with Macbeth?", "Hecate: Security is mortals' chiefest enemy.", "Hecate: He shall spurn fate.", "Witches: We obey."], "questions": [("Hecate plans to mislead Macbeth.", True), ("Hecate helps Macduff in this scene.", False)]},
        {"title": "Scene 6 - Resistance", "script": ["Lennox: Things have been strangely borne.", "Lord: Macduff is gone to England.", "Lennox: Suffering country under a hand accursed.", "Lord: Hope rises in rebellion."], "questions": [("Macduff seeks support in England.", True), ("Lennox praises Macbeth's fair rule.", False)]},
    ]},
    {"name": "Act 4", "rect": pygame.Rect(700, 190, 190, 100), "scenes": [
        {"title": "Scene 1 - Apparitions", "script": ["Witches: Double, double toil and trouble.", "Apparition: Beware Macduff.", "Apparition: None of woman born shall harm Macbeth.", "Apparition: Birnam Wood must come to Dunsinane.", "Macbeth: The firstlings of my heart shall be the firstlings of my hand."], "questions": [("The prophecies make Macbeth overconfident.", True), ("The apparitions tell Macbeth to surrender.", False)]},
        {"title": "Scene 2 - Macduff's Castle", "script": ["Lady Macduff: He loves us not.", "Messenger: Flee from this place.", "Murderer: What, you egg!", "Lady Macduff: Murder!", "Child: Run!"], "questions": [("Macbeth's men kill Macduff's family.", True), ("Lady Macduff escapes safely with everyone.", False)]},
        {"title": "Scene 3 - England", "script": ["Malcolm: This tyrant blisters our tongues.", "Macduff: Bleed, bleed, poor country.", "Ross: Your wife and babes were slaughtered.", "Macduff: All my pretty ones?", "Malcolm: Be this the whetstone of your sword."], "questions": [("Macduff learns his family was murdered.", True), ("Macduff forgives Macbeth and makes peace.", False)]},
    ]},
    {"name": "Act 5", "rect": pygame.Rect(390, 330, 320, 120), "scenes": [
        {"title": "Scene 1 - Sleepwalking", "script": ["Doctor: I have watched two nights.", "Gentlewoman: Lo, here she comes.", "Lady Macbeth: Out, damned spot!", "Doctor: More needs she the divine than the physician."], "questions": [("Lady Macbeth reveals guilt while sleepwalking.", True), ("The doctor cures Lady Macbeth completely.", False)]},
        {"title": "Scene 2 - Rebels Gather", "script": ["Menteith: The English power is near.", "Angus: His title hangs loose about him.", "Caithness: We march to join Malcolm.", "All: On to Dunsinane."], "questions": [("Scottish nobles join Malcolm.", True), ("The thanes think Macbeth is beloved.", False)]},
        {"title": "Scene 3 - Dunsinane", "script": ["Macbeth: Bring me no more reports.", "Doctor: She is troubled.", "Macbeth: Canst thou not minister to a mind diseased?", "Servant: The enemy approaches."], "questions": [("Macbeth asks for treatment for Lady Macbeth's mind.", True), ("Macbeth plans to flee immediately.", False)]},
        {"title": "Scene 4 - Birnam Branches", "script": ["Malcolm: Let every soldier cut down a bough.", "Soldier: We shall shadow our numbers.", "Siward: The time approaches.", "Army: Forward."], "questions": [("Malcolm uses branches to hide army size.", True), ("Malcolm cancels the attack.", False)]},
        {"title": "Scene 5 - Tomorrow", "script": ["Seyton: The queen, my lord, is dead.", "Macbeth: She should have died hereafter.", "Macbeth: Tomorrow, and tomorrow, and tomorrow...", "Macbeth: Life's but a walking shadow."], "questions": [("Macbeth gives the 'Tomorrow' speech.", True), ("Macbeth celebrates Lady Macbeth's death.", False)]},
        {"title": "Scene 6 - Battle Begins", "script": ["Malcolm: Throw down your leavy screens.", "Siward: Make all our trumpets speak.", "Macduff: Lead me to the tyrant.", "Soldier: The battle begins."], "questions": [("The army drops branches before battle.", True), ("Macduff refuses to fight.", False)]},
        {"title": "Scene 7 - Young Siward", "script": ["Young Siward: What is thy name?", "Macbeth: My name's Macbeth.", "Young Siward: A hateful name.", "Macbeth: Thou wast born of woman."], "questions": [("Macbeth kills Young Siward.", True), ("Young Siward defeats Macbeth.", False)]},
        {"title": "Scene 8 - Final Duel", "script": ["Macduff: Turn, hell-hound, turn!", "Macbeth: I bear a charmed life.", "Macduff: I was from my mother's womb untimely ripped.", "Macbeth: I'll not yield.", "Herald: Macbeth has fallen; Malcolm reigns."], "questions": [("Macduff reveals he was not born in the usual way.", True), ("Macbeth keeps the throne at the end.", False)]},
    ]},
]


def draw_text(surface, text, font, color, x, y):
    surface.blit(font.render(text, True, color), (x, y))


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=6):
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        test = cur + word + " "
        if font.size(test)[0] <= rect.width - 10:
            cur = test
        else:
            lines.append(cur)
            cur = word + " "
    lines.append(cur)
    y = rect.y + 8
    for line in lines:
        surface.blit(font.render(line.strip(), True, color), (rect.x + 8, y))
        y += font.get_height() + line_spacing


def parse_script_line(line):
    if ":" in line:
        spk, txt = line.split(":", 1)
        return spk.strip(), txt.strip()
    return "Narrator", line


def draw_person(surface, x, y, color, scale=1.0):
    hr = int(10 * scale)
    bl = int(24 * scale)
    al = int(14 * scale)
    ll = int(18 * scale)
    pygame.draw.circle(surface, color, (x, y), hr)
    pygame.draw.line(surface, color, (x, y + hr), (x, y + hr + bl), 3)
    pygame.draw.line(surface, color, (x - al, y + hr + 8), (x + al, y + hr + 8), 3)
    pygame.draw.line(surface, color, (x, y + hr + bl), (x - ll // 2, y + hr + bl + ll), 3)
    pygame.draw.line(surface, color, (x, y + hr + bl), (x + ll // 2, y + hr + bl + ll), 3)


def draw_speech_bubble(surface, text, font, x, y):
    rect = pygame.Rect(x - 170, y - 78, 340, 62)
    pygame.draw.rect(surface, WHITE, rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10)
    pygame.draw.polygon(surface, WHITE, [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)])
    pygame.draw.polygon(surface, BLACK, [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)], 2)
    draw_wrapped_text(surface, text, font, BLACK, rect, line_spacing=2)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Macbeth Walkthrough Quiz Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("georgia", 58, bold=True)
    subtitle = pygame.font.SysFont("georgia", 28, bold=True)
    font = pygame.font.SysFont("cambria", 24)
    small = pygame.font.SysFont("cambria", 20)
    tiny = pygame.font.SysFont("cambria", 18)

    state = "menu"
    player = pygame.Rect(100, 560, 30, 30)
    selected_act_idx = None
    selected_scene_idx = 0
    selected_scene_cursor = 0
    scene_line_idx = 0
    question_idx = 0
    feedback = ""
    last_completed_scene = ""
    last_completed_act = ""

    rapid_order = list(range(len(RAPID_QUIZ)))
    rapid_idx = 0
    rapid_start_ms = 0
    rapid_score = 0
    rapid_answered = 0
    rapid_feedback = ""

    scene_score = 0
    total_scene_questions = sum(len(scene["questions"]) for act in ACTS for scene in act["scenes"])
    completed_acts = set()
    completed_scenes = {i: set() for i in range(len(ACTS))}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and state != "menu":
                    state = "menu"
                    selected_act_idx = None
                    continue

                if state == "menu":
                    if event.key in (pygame.K_1, pygame.K_q):
                        random.shuffle(rapid_order)
                        rapid_idx = 0
                        rapid_score = 0
                        rapid_answered = 0
                        rapid_feedback = ""
                        rapid_start_ms = pygame.time.get_ticks()
                        state = "rapid_quiz"
                    elif event.key in (pygame.K_2, pygame.K_m, pygame.K_RETURN, pygame.K_SPACE):
                        state = "map"
                elif state == "rapid_quiz":
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        choice = event.key - pygame.K_1
                        q = RAPID_QUIZ[rapid_order[rapid_idx]]
                        if choice == q["answer"]:
                            rapid_score += 1
                            rapid_feedback = "Correct"
                        else:
                            rapid_feedback = f"Wrong (answer: {q['choices'][q['answer']]})"
                        rapid_answered += 1
                        rapid_idx = (rapid_idx + 1) % len(rapid_order)
                elif state == "map":
                    if event.key == pygame.K_e:
                        for idx, act in enumerate(ACTS):
                            if player.colliderect(act["rect"]):
                                selected_act_idx = idx
                                selected_scene_cursor = 0
                                state = "scene_select"
                                break
                elif state == "scene_select":
                    act = ACTS[selected_act_idx]
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_scene_cursor = (selected_scene_cursor - 1) % len(act["scenes"])
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_scene_cursor = (selected_scene_cursor + 1) % len(act["scenes"])
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected_scene_idx = selected_scene_cursor
                        scene_line_idx = 0
                        question_idx = 0
                        feedback = ""
                        state = "scene"
                elif state == "scene":
                    if event.key == pygame.K_SPACE:
                        scene = ACTS[selected_act_idx]["scenes"][selected_scene_idx]
                        scene_line_idx += 1
                        if scene_line_idx >= len(scene["script"]):
                            scene_line_idx = len(scene["script"]) - 1
                            question_idx = 0
                            feedback = ""
                            state = "question"
                elif state == "question":
                    if event.key in (pygame.K_t, pygame.K_f):
                        scene = ACTS[selected_act_idx]["scenes"][selected_scene_idx]
                        _, answer = scene["questions"][question_idx]
                        ok = (event.key == pygame.K_t) == answer
                        if ok:
                            scene_score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong. Correct: {'True' if answer else 'False'}"
                        question_idx += 1
                        if question_idx >= len(scene["questions"]):
                            completed_scenes[selected_act_idx].add(selected_scene_idx)
                            last_completed_scene = scene["title"]
                            if len(completed_scenes[selected_act_idx]) == len(ACTS[selected_act_idx]["scenes"]):
                                completed_acts.add(selected_act_idx)
                                last_completed_act = ACTS[selected_act_idx]["name"]
                            state = "scene_complete"
                elif state == "scene_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if len(completed_acts) == len(ACTS):
                            state = "end"
                        elif selected_act_idx in completed_acts:
                            state = "act_complete"
                        else:
                            state = "scene_select"
                elif state == "act_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        state = "map"
                elif state == "end":
                    if event.key == pygame.K_r:
                        scene_score = 0
                        rapid_score = 0
                        rapid_answered = 0
                        completed_acts = set()
                        completed_scenes = {i: set() for i in range(len(ACTS))}
                        player.topleft = (100, 560)
                        state = "menu"

        if state == "rapid_quiz":
            if (pygame.time.get_ticks() - rapid_start_ms) / 1000.0 >= RAPID_TIME_SECONDS:
                state = "rapid_result"
        elif state == "map":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED
            player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        screen.fill(BG)

        total_score = rapid_score + scene_score
        header = pygame.Rect(20, 18, WIDTH - 40, 96)
        if state != "menu":
            pygame.draw.rect(screen, PANEL_DARK, header, border_radius=14)
            pygame.draw.rect(screen, WHITE, header, 2, border_radius=14)
            draw_text(screen, "Macbeth Interactive Scenes", subtitle, WHITE, 350, 32)
            draw_text(screen, f"Total Score: {total_score}/{len(RAPID_QUIZ) + total_scene_questions}", font, WHITE, 28, 82)
            draw_text(screen, f"Acts Completed: {len(completed_acts)}/5", font, WHITE, 840, 82)
            draw_text(screen, "ESC = Main Menu", tiny, WHITE, 30, 58)
            draw_text(screen, "Created by Justin Girard", tiny, WHITE, 900, 670)

        if state == "menu":
            panel = pygame.Rect(130, 120, 840, 430)
            pygame.draw.rect(screen, PANEL_DARK, panel, border_radius=18)
            pygame.draw.rect(screen, ACCENT, panel, 3, border_radius=18)
            draw_text(screen, "MACBETH", title_font, WHITE, 380, 170)
            draw_text(screen, "Main Menu", subtitle, ACCENT, 455, 255)
            draw_text(screen, "1) Rapid Multiple Choice (30 sec)", font, WHITE, 330, 340)
            draw_text(screen, "2) Mini Map (Acts and Scenes)", font, WHITE, 355, 385)
            draw_text(screen, "Press 1 or 2 to choose.", small, WHITE, 420, 435)
            draw_text(screen, "Created by Justin Girard", tiny, WHITE, 900, 670)

        elif state == "rapid_quiz":
            remain = max(0, RAPID_TIME_SECONDS - int((pygame.time.get_ticks() - rapid_start_ms) / 1000))
            panel = pygame.Rect(120, 150, 860, 430)
            pygame.draw.rect(screen, PANEL, panel, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel, 2, border_radius=12)
            q = RAPID_QUIZ[rapid_order[rapid_idx]]
            draw_text(screen, "Rapid Mixed Quiz", subtitle, ACCENT, 430, 170)
            draw_text(screen, f"Time: {remain}s", font, WHITE, 160, 170)
            draw_text(screen, f"Answered: {rapid_answered}", font, WHITE, 850, 170)
            draw_wrapped_text(screen, q["q"], font, WHITE, pygame.Rect(160, 230, 780, 80))
            for i, c in enumerate(q["choices"], start=1):
                draw_text(screen, f"{i}) {c}", small, WHITE, 190, 300 + (i - 1) * 46)
            draw_text(screen, "Press 1-4 to answer quickly.", small, WHITE, 400, 500)
            if rapid_feedback:
                draw_text(screen, rapid_feedback, small, GOOD if rapid_feedback == "Correct" else BAD, 430, 540)

        elif state == "rapid_result":
            draw_text(screen, "Rapid Quiz Complete!", subtitle, GOOD, 395, 230)
            draw_text(screen, f"Score: {rapid_score}/{max(1, rapid_answered)}", font, WHITE, 460, 290)
            draw_text(screen, "Press ESC to return to Main Menu.", font, WHITE, 340, 350)
            draw_text(screen, "Or continue to Mini Map with 2.", small, WHITE, 420, 395)

        elif state == "map":
            draw_text(screen, "Move: WASD/Arrows | Press E on an act", font, WHITE, 320, 128)
            for idx, act in enumerate(ACTS):
                base = ZONE_DONE if idx in completed_acts else ZONE_COLOR
                color = ZONE_HOVER if player.colliderect(act["rect"]) else base
                pygame.draw.rect(screen, color, act["rect"], border_radius=10)
                pygame.draw.rect(screen, BLACK, act["rect"], 2, border_radius=10)
                draw_text(screen, act["name"], font, BLACK, act["rect"].x + 54, act["rect"].y + 20)
                draw_text(screen, f"{len(act['scenes'])} scenes", tiny, BLACK, act["rect"].x + 52, act["rect"].y + 55)
                draw_text(screen, f"Done: {len(completed_scenes[idx])}/{len(act['scenes'])}", tiny, BLACK, act["rect"].x + 52, act["rect"].y + 74)
            draw_person(screen, player.centerx, player.y + 6, PLAYER_COLOR, 1.05)
            draw_text(screen, "You", small, WHITE, player.x - 2, player.y - 22)

        elif state == "scene_select":
            act = ACTS[selected_act_idx]
            draw_text(screen, f"{act['name']} - Scene Select", subtitle, WHITE, 390, 126)
            draw_text(screen, "UP/DOWN choose | ENTER play", small, WHITE, 395, 160)
            panel = pygame.Rect(160, 200, 780, 410)
            pygame.draw.rect(screen, PANEL, panel, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel, 2, border_radius=12)
            start = max(0, selected_scene_cursor - 8)
            for i, scene in enumerate(act["scenes"][start:start + 12]):
                real = start + i
                marker = ">" if real == selected_scene_cursor else " "
                status = " [Complete]" if real in completed_scenes[selected_act_idx] else ""
                draw_text(screen, f"{marker} {real + 1}. {scene['title']}{status}", tiny, ACCENT if real == selected_scene_cursor else WHITE, 185, 225 + i * 30)

        elif state == "scene":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} | {scene['title']}", font, WHITE, 220, 128)
            stage = pygame.Rect(120, 160, 860, 340)
            pygame.draw.rect(screen, PANEL, stage, border_radius=12)
            pygame.draw.rect(screen, WHITE, stage, 2, border_radius=12)
            pygame.draw.rect(screen, (70, 58, 50), pygame.Rect(140, 440, 820, 40), border_radius=8)
            speakers = []
            for line in scene["script"]:
                s, _ = parse_script_line(line)
                if s not in speakers:
                    speakers.append(s)
            spacing = 820 // (len(speakers) + 1) if speakers else 410
            pos = {}
            for i, s in enumerate(speakers, start=1):
                pos[s] = (140 + spacing * i, 345)
            palette = [(221, 117, 117), (120, 176, 240), (136, 206, 152), (224, 190, 103), (196, 145, 230)]
            for i, s in enumerate(speakers):
                x, y = pos[s]
                draw_person(screen, x, y, palette[i % len(palette)], 1.0)
                draw_text(screen, s, tiny, WHITE, x - 45, y + 58)
            cur = scene["script"][scene_line_idx]
            speaker, spoken = parse_script_line(cur)
            if speaker in pos:
                x, y = pos[speaker]
                draw_speech_bubble(screen, spoken, tiny, x, y - 10)
            draw_text(screen, "SPACE = next line", font, WHITE, 430, 560)

        elif state == "question":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} Quiz | {scene['title']}", font, WHITE, 220, 128)
            panel = pygame.Rect(120, 180, 860, 320)
            pygame.draw.rect(screen, PANEL, panel, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel, 2, border_radius=12)
            statement, _ = scene["questions"][question_idx]
            draw_wrapped_text(screen, statement, font, WHITE, pygame.Rect(150, 220, 800, 160))
            draw_text(screen, "Press T for True or F for False", font, WHITE, 360, 430)
            if feedback:
                draw_text(screen, feedback, font, GOOD if feedback.startswith("Correct") else BAD, 300, 470)

        elif state == "scene_complete":
            draw_text(screen, "Scene Complete!", subtitle, GOOD, 430, 215)
            draw_text(screen, last_completed_scene, font, WHITE, 210, 270)
            draw_text(screen, "Press ENTER to continue.", font, WHITE, 410, 330)

        elif state == "act_complete":
            draw_text(screen, f"{last_completed_act} Complete!", subtitle, GOOD, 400, 215)
            draw_text(screen, "Every scene in this act is done.", font, WHITE, 400, 275)
            draw_text(screen, "Press ENTER to go back to map.", font, WHITE, 380, 335)

        elif state == "end":
            draw_text(screen, "The Full Play Is Complete!", subtitle, WHITE, 330, 175)
            draw_text(screen, f"Rapid Quiz: {rapid_score}/{max(1, rapid_answered)}", font, WHITE, 420, 240)
            draw_text(screen, f"Scene Quiz: {scene_score}/{total_scene_questions}", font, WHITE, 420, 280)
            draw_text(screen, "Press R to reset progress.", font, WHITE, 420, 340)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
import random
import sys
import pygame


WIDTH, HEIGHT = 1100, 700
FPS = 60
PLAYER_SPEED = 4
RAPID_TIME_SECONDS = 30

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
BG = (20, 23, 30)
PLAYER_COLOR = (90, 180, 255)
ZONE_COLOR = (102, 205, 149)
ZONE_HOVER = (255, 210, 90)
ZONE_DONE = (120, 130, 145)
PANEL = (48, 52, 63)
PANEL_DARK = (32, 36, 46)
GOOD = (70, 190, 110)
BAD = (210, 90, 90)
ACCENT = (188, 152, 88)


RAPID_QUIZ = [
    {"q": "Who gives Macbeth the first prophecy?", "choices": ["Macduff", "The Witches", "Duncan", "Banquo"], "answer": 1},
    {"q": "Who is murdered in Act 2?", "choices": ["Banquo", "Malcolm", "King Duncan", "Macduff"], "answer": 2},
    {"q": "Who sees Banquo's ghost?", "choices": ["Lady Macbeth", "Macbeth", "Macduff", "Ross"], "answer": 1},
    {"q": "What forest appears to move toward Dunsinane?", "choices": ["Sherwood", "Birnam Wood", "Arden", "Caledon"], "answer": 1},
    {"q": "Who says 'Out, damned spot!'?", "choices": ["Lady Macbeth", "Witch 1", "Hecate", "Lady Macduff"], "answer": 0},
    {"q": "Who kills Macbeth?", "choices": ["Malcolm", "Banquo", "Macduff", "Siward"], "answer": 2},
    {"q": "Who becomes king at the end?", "choices": ["Macduff", "Malcolm", "Fleance", "Donalbain"], "answer": 1},
    {"q": "What title is Macbeth given early on?", "choices": ["Thane of Cawdor", "Duke of York", "Prince of Wales", "Earl of Fife"], "answer": 0},
]


ACTS = [
    {
        "name": "Act 1",
        "rect": pygame.Rect(70, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - The Witches on the Heath", "script": ["Witch 1: When shall we three meet again, in thunder, lightning, or in rain?", "Witch 2: When the hurlyburly's done, when the battle's lost and won.", "Witch 3: That will be ere the set of sun.", "All Witches: Fair is foul, and foul is fair."], "questions": [("The witches appear before Macbeth is seen.", True), ("The witches say weather will remain peaceful.", False)]},
            {"title": "Scene 2 - Report from Battle", "script": ["Captain: For brave Macbeth, well he deserves that name.", "Duncan: O valiant cousin, worthy gentleman.", "Ross: The thane of Cawdor has betrayed us.", "Duncan: What he hath lost, noble Macbeth hath won."], "questions": [("Duncan rewards Macbeth with Cawdor's title.", True), ("Macbeth is punished for cowardice in this scene.", False)]},
            {"title": "Scene 3 - Prophecies Given", "script": ["Witch 1: All hail, Macbeth, thane of Glamis!", "Witch 2: All hail, Macbeth, thane of Cawdor!", "Witch 3: All hail, Macbeth, that shalt be king hereafter!", "Banquo: You shall get kings, though you be none."], "questions": [("The witches also predict Banquo's descendants will be kings.", True), ("Macbeth immediately rejects all ambition here.", False)]},
            {"title": "Scene 4 - Prince of Cumberland", "script": ["Duncan: We will establish our estate upon our eldest, Malcolm.", "Macbeth: The Prince of Cumberland is a step I must o'erleap.", "Macbeth: Stars, hide your fires; let not light see my black and deep desires.", "Banquo: New honors come upon him."], "questions": [("Malcolm is named Prince of Cumberland.", True), ("Macbeth openly tells Duncan he wants the throne.", False)]},
            {"title": "Scene 5 - Lady Macbeth Reads", "script": ["Lady Macbeth: Yet do I fear thy nature; it is too full o' the milk of human kindness.", "Lady Macbeth: Come, you spirits, unsex me here.", "Messenger: The king comes here tonight.", "Lady Macbeth: Leave all the rest to me."], "questions": [("Lady Macbeth calls on spirits to harden her.", True), ("Lady Macbeth wants Macbeth to stay innocent and passive.", False)]},
            {"title": "Scene 6 - Duncan at Inverness", "script": ["Duncan: This castle hath a pleasant seat.", "Banquo: The heaven's breath smells wooingly here.", "Lady Macbeth: All our service in every point twice done and then done double.", "Duncan: Fair and noble hostess, we are your guest tonight."], "questions": [("Duncan feels safe at Macbeth's castle.", True), ("Banquo warns Duncan to leave immediately.", False)]},
            {"title": "Scene 7 - Macbeth Decides", "script": ["Macbeth: We will proceed no further in this business.", "Lady Macbeth: When you durst do it, then you were a man.", "Macbeth: I am settled, and bend up each corporal agent to this terrible feat.", "Lady Macbeth: False face must hide what the false heart doth know."], "questions": [("Lady Macbeth persuades Macbeth to continue the murder plan.", True), ("Macbeth decides to confess to Duncan instead.", False)]},
        ],
    },
    {
        "name": "Act 2",
        "rect": pygame.Rect(280, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Dagger Soliloquy", "script": ["Banquo: I dreamt last night of the three weird sisters.", "Macbeth: Is this a dagger which I see before me, the handle toward my hand?", "Macbeth: Thou marshall'st me the way that I was going.", "Bell: Ringing in the distance."], "questions": [("Macbeth hallucinates a dagger before the murder.", True), ("Banquo orders Macbeth to kill Duncan.", False)]},
            {"title": "Scene 2 - Duncan Murdered", "script": ["Lady Macbeth: That which hath made them drunk hath made me bold.", "Macbeth: I have done the deed.", "Macbeth: I heard a voice cry 'Sleep no more!'", "Lady Macbeth: A little water clears us of this deed."], "questions": [("Macbeth hears imaginary voices after killing Duncan.", True), ("Lady Macbeth says they should immediately surrender.", False)]},
            {"title": "Scene 3 - The Porter and Discovery", "script": ["Porter: Knock, knock! Who's there?", "Macduff: O horror, horror, horror!", "Macbeth: Had I but died an hour before this chance...", "Donalbain: There's daggers in men's smiles."], "questions": [("Macduff discovers Duncan's body.", True), ("Duncan's sons decide to stay in Scotland for safety.", False)]},
            {"title": "Scene 4 - Unnatural Signs", "script": ["Old Man: 'Tis day, and yet dark night strangles the traveling lamp.", "Ross: Duncan's horses turned wild in nature.", "Macduff: Those that Macbeth hath slain.", "Ross: The heavens are troubled with man's bloody act."], "questions": [("Nature behaves strangely after Duncan's murder.", True), ("Macduff attends Macbeth's coronation at Scone.", False)]},
        ],
    },
    {
        "name": "Act 3",
        "rect": pygame.Rect(490, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Banquo Suspects Macbeth", "script": ["Banquo: Thou hast it now: king, Cawdor, Glamis.", "Macbeth: Our fears in Banquo stick deep.", "Macbeth: Banquo, thy soul's flight must find heaven tonight.", "Murderers: We are resolved."], "questions": [("Macbeth arranges Banquo's murder.", True), ("Banquo fully trusts Macbeth's rule.", False)]},
            {"title": "Scene 2 - Macbeth's Fear Deepens", "script": ["Lady Macbeth: Naught's had, all's spent.", "Macbeth: O, full of scorpions is my mind, dear wife.", "Macbeth: Things bad begun make strong themselves by ill.", "Lady Macbeth: You must leave this."], "questions": [("Macbeth tells Lady Macbeth he is mentally tormented.", True), ("Lady Macbeth knows every detail of Banquo's ambush plan.", False)]},
            {"title": "Scene 3 - Banquo Ambushed", "script": ["Murderer: Stand to't.", "Banquo: O treachery! Fly, good Fleance!", "Murderer: Who did strike out the light?", "Murderer: Fleance is escaped."], "questions": [("Fleance escapes while Banquo is killed.", True), ("Banquo kills all the murderers and survives.", False)]},
            {"title": "Scene 4 - Banquet and Ghost", "script": ["Macbeth: The table's full.", "Macbeth: Never shake thy gory locks at me.", "Lady Macbeth: Are you a man?", "Lords: The king is troubled."], "questions": [("Macbeth sees Banquo's ghost at the banquet.", True), ("The guests can all see the ghost too.", False)]},
            {"title": "Scene 5 - Hecate's Rebuke", "script": ["Hecate: How did you dare to trade and traffic with Macbeth?", "Hecate: Security is mortals' chiefest enemy.", "Hecate: He shall spurn fate and scorn death.", "Witches: We obey."], "questions": [("Hecate plans to lure Macbeth into false confidence.", True), ("Hecate orders the witches to help Macduff.", False)]},
            {"title": "Scene 6 - Lennox and the Lord", "script": ["Lennox: Things have been strangely borne.", "Lord: Macduff is gone to England for aid.", "Lennox: Suffering country, under a hand accursed.", "Lord: Hope rises in rebellion."], "questions": [("Macduff seeks help from England.", True), ("Lennox openly praises Macbeth as a just ruler.", False)]},
        ],
    },
    {
        "name": "Act 4",
        "rect": pygame.Rect(700, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Apparitions and Warnings", "script": ["Witches: Double, double toil and trouble.", "Apparition: Beware Macduff.", "Apparition: None of woman born shall harm Macbeth.", "Apparition: Birnam Wood must come to Dunsinane.", "Macbeth: The firstlings of my heart shall be the firstlings of my hand."], "questions": [("The prophecies make Macbeth overconfident.", True), ("The apparitions tell Macbeth to surrender the crown.", False)]},
            {"title": "Scene 2 - Macduff's Castle Attacked", "script": ["Lady Macduff: He loves us not.", "Messenger: Flee from this place.", "Murderer: What, you egg!", "Lady Macduff: Murder!", "Child: Run!"], "questions": [("Macbeth's men kill Macduff's family.", True), ("Lady Macduff escapes safely with all her children.", False)]},
            {"title": "Scene 3 - England: Grief and Alliance", "script": ["Malcolm: This tyrant blisters our tongues.", "Macduff: Bleed, bleed, poor country.", "Ross: Your wife and babes were slaughtered.", "Macduff: All my pretty ones? Did you say all?", "Malcolm: Be this the whetstone of your sword."], "questions": [("Macduff learns his family has been murdered.", True), ("Macduff decides to forgive Macbeth and make peace.", False)]},
        ],
    },
    {
        "name": "Act 5",
        "rect": pygame.Rect(390, 330, 320, 120),
        "scenes": [
            {"title": "Scene 1 - Sleepwalking", "script": ["Doctor: I have watched two nights.", "Gentlewoman: Lo, here she comes.", "Lady Macbeth: Out, damned spot!", "Doctor: More needs she the divine than the physician."], "questions": [("Lady Macbeth reveals guilt while sleepwalking.", True), ("The doctor fully cures Lady Macbeth here.", False)]},
            {"title": "Scene 2 - Rebel Forces Gather", "script": ["Menteith: The English power is near.", "Angus: Now does he feel his title hang loose about him.", "Caithness: We march to join Malcolm.", "All: On to Dunsinane."], "questions": [("Scottish nobles join Malcolm against Macbeth.", True), ("The thanes think Macbeth is a beloved king.", False)]},
            {"title": "Scene 3 - Macbeth at Dunsinane", "script": ["Macbeth: Bring me no more reports.", "Doctor: She is troubled with thick-coming fancies.", "Macbeth: Canst thou not minister to a mind diseased?", "Servant: The enemy approaches."], "questions": [("Macbeth asks for medical help for Lady Macbeth's mind.", True), ("Macbeth plans to flee immediately.", False)]},
            {"title": "Scene 4 - Branches from Birnam", "script": ["Malcolm: Let every soldier cut down a bough.", "Soldier: We shall shadow our numbers.", "Siward: The time approaches.", "Army: Forward."], "questions": [("Malcolm uses tree branches to hide troop numbers.", True), ("Malcolm decides not to attack Dunsinane.", False)]},
            {"title": "Scene 5 - Tomorrow Speech", "script": ["Seyton: The queen, my lord, is dead.", "Macbeth: She should have died hereafter.", "Macbeth: Tomorrow, and tomorrow, and tomorrow...", "Macbeth: Life's but a walking shadow."], "questions": [("Macbeth delivers his 'Tomorrow' soliloquy.", True), ("Macbeth celebrates joyfully at Lady Macbeth's death.", False)]},
            {"title": "Scene 6 - Battle Lines Drawn", "script": ["Malcolm: Throw down your leavy screens.", "Siward: Make all our trumpets speak.", "Macduff: Lead me where the tyrant is.", "Soldier: The battle begins."], "questions": [("Malcolm's army drops their branches before battle.", True), ("Macduff refuses to fight anyone.", False)]},
            {"title": "Scene 7 - Young Siward and Macbeth", "script": ["Young Siward: What is thy name?", "Macbeth: My name's Macbeth.", "Young Siward: The devil himself could not pronounce a title more hateful.", "Macbeth: Thou wast born of woman."], "questions": [("Macbeth kills Young Siward.", True), ("Young Siward defeats Macbeth here.", False)]},
            {"title": "Scene 8 - Macduff's Challenge", "script": ["Macduff: Turn, hell-hound, turn!", "Macbeth: I bear a charmed life.", "Macduff: I was from my mother's womb untimely ripped.", "Macbeth: I'll not yield.", "Herald: Macbeth has fallen; Malcolm reigns."], "questions": [("Macduff reveals he was not born in the usual way.", True), ("Macbeth survives and keeps the throne.", False)]},
        ],
    },
]


def parse_script_line(line):
    if ":" in line:
        speaker, text = line.split(":", 1)
        return speaker.strip(), text.strip()
    return "Narrator", line


def draw_person(surface, x, y, body_color, scale=1.0):
    head_radius = int(10 * scale)
    body_len = int(24 * scale)
    arm_len = int(14 * scale)
    leg_len = int(18 * scale)
    pygame.draw.circle(surface, body_color, (x, y), head_radius)
    pygame.draw.line(surface, body_color, (x, y + head_radius), (x, y + head_radius + body_len), 3)
    pygame.draw.line(surface, body_color, (x - arm_len, y + head_radius + 8), (x + arm_len, y + head_radius + 8), 3)
    pygame.draw.line(surface, body_color, (x, y + head_radius + body_len), (x - leg_len // 2, y + head_radius + body_len + leg_len), 3)
    pygame.draw.line(surface, body_color, (x, y + head_radius + body_len), (x + leg_len // 2, y + head_radius + body_len + leg_len), 3)


def draw_text(surface, text, font, color, x, y):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=6):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= rect.width - 10:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)
    y = rect.y + 8
    for line in lines:
        img = font.render(line.strip(), True, color)
        surface.blit(img, (rect.x + 8, y))
        y += font.get_height() + line_spacing


def draw_speech_bubble(surface, text, font, x, y):
    bubble_rect = pygame.Rect(x - 170, y - 78, 340, 62)
    pygame.draw.rect(surface, WHITE, bubble_rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, bubble_rect, 2, border_radius=10)
    pygame.draw.polygon(surface, WHITE, [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)])
    pygame.draw.polygon(surface, BLACK, [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)], 2)
    draw_wrapped_text(surface, text, font, BLACK, bubble_rect, line_spacing=2)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Macbeth Walkthrough Quiz Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("georgia", 58, bold=True)
    subtitle_font = pygame.font.SysFont("georgia", 28, bold=True)
    font = pygame.font.SysFont("cambria", 24)
    small_font = pygame.font.SysFont("cambria", 20)
    tiny_font = pygame.font.SysFont("cambria", 18)

    player = pygame.Rect(100, 560, 30, 30)
    scene_score = 0
    rapid_score = 0
    rapid_answered = 0
    total_scene_questions = sum(len(scene["questions"]) for act in ACTS for scene in act["scenes"])

    state = "title"
    selected_act_idx = None
    selected_scene_idx = 0
    selected_scene_cursor = 0
    scene_line_idx = 0
    question_idx = 0
    feedback = ""
    completed_acts = set()
    completed_scenes = {i: set() for i in range(len(ACTS))}
    last_completed_scene = ""
    last_completed_act = ""

    rapid_order = list(range(len(RAPID_QUIZ)))
    random.shuffle(rapid_order)
    rapid_idx = 0
    rapid_start_ms = 0
    rapid_feedback = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "title":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        random.shuffle(rapid_order)
                        rapid_idx = 0
                        rapid_score = 0
                        rapid_answered = 0
                        rapid_feedback = ""
                        rapid_start_ms = pygame.time.get_ticks()
                        state = "rapid_quiz"
                elif state == "rapid_quiz":
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        choice = event.key - pygame.K_1
                        q = RAPID_QUIZ[rapid_order[rapid_idx]]
                        if choice == q["answer"]:
                            rapid_score += 1
                            rapid_feedback = "Correct"
                        else:
                            rapid_feedback = f"Wrong (answer: {q['choices'][q['answer']]})"
                        rapid_answered += 1
                        rapid_idx = (rapid_idx + 1) % len(rapid_order)
                    elif event.key == pygame.K_ESCAPE:
                        state = "map"
                elif state == "map":
                    if event.key == pygame.K_e:
                        for idx, act in enumerate(ACTS):
                            if player.colliderect(act["rect"]):
                                selected_act_idx = idx
                                selected_scene_cursor = 0
                                state = "scene_select"
                                break
                elif state == "scene_select":
                    act = ACTS[selected_act_idx]
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_scene_cursor = (selected_scene_cursor - 1) % len(act["scenes"])
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_scene_cursor = (selected_scene_cursor + 1) % len(act["scenes"])
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected_scene_idx = selected_scene_cursor
                        scene_line_idx = 0
                        question_idx = 0
                        feedback = ""
                        state = "scene"
                    elif event.key == pygame.K_ESCAPE:
                        selected_act_idx = None
                        state = "map"
                elif state == "scene":
                    if event.key == pygame.K_SPACE:
                        act = ACTS[selected_act_idx]
                        scene = act["scenes"][selected_scene_idx]
                        scene_line_idx += 1
                        if scene_line_idx >= len(scene["script"]):
                            scene_line_idx = len(scene["script"]) - 1
                            question_idx = 0
                            feedback = ""
                            state = "question"
                elif state == "question":
                    if event.key in (pygame.K_t, pygame.K_f):
                        act = ACTS[selected_act_idx]
                        scene = act["scenes"][selected_scene_idx]
                        _, answer = scene["questions"][question_idx]
                        user_answer = event.key == pygame.K_t
                        if user_answer == answer:
                            scene_score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong. Correct answer: {'True' if answer else 'False'}"

                        question_idx += 1
                        if question_idx >= len(scene["questions"]):
                            completed_scenes[selected_act_idx].add(selected_scene_idx)
                            last_completed_scene = scene["title"]
                            if len(completed_scenes[selected_act_idx]) == len(act["scenes"]):
                                completed_acts.add(selected_act_idx)
                                last_completed_act = act["name"]
                            state = "scene_complete"
                elif state == "scene_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if len(completed_acts) == len(ACTS):
                            state = "end"
                        elif selected_act_idx in completed_acts:
                            state = "act_complete"
                        else:
                            state = "scene_select"
                elif state == "act_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_m):
                        selected_act_idx = None
                        state = "map"
                elif state == "end":
                    if event.key == pygame.K_r:
                        scene_score = 0
                        rapid_score = 0
                        rapid_answered = 0
                        selected_act_idx = None
                        selected_scene_idx = 0
                        selected_scene_cursor = 0
                        scene_line_idx = 0
                        question_idx = 0
                        feedback = ""
                        completed_acts = set()
                        completed_scenes = {i: set() for i in range(len(ACTS))}
                        last_completed_scene = ""
                        last_completed_act = ""
                        player.topleft = (100, 560)
                        state = "title"
                    elif event.key == pygame.K_m:
                        selected_act_idx = None
                        state = "map"

        if state == "rapid_quiz":
            elapsed = (pygame.time.get_ticks() - rapid_start_ms) / 1000.0
            if elapsed >= RAPID_TIME_SECONDS:
                state = "map"

        keys = pygame.key.get_pressed()
        if state == "map":
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED
            player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        screen.fill(BG)

        total_score = rapid_score + scene_score

        if state == "title":
            title_panel = pygame.Rect(130, 120, 840, 430)
            pygame.draw.rect(screen, PANEL_DARK, title_panel, border_radius=18)
            pygame.draw.rect(screen, ACCENT, title_panel, 3, border_radius=18)
            draw_text(screen, "MACBETH", title_font, WHITE, 380, 170)
            draw_text(screen, "Interactive Scene Journey", subtitle_font, ACCENT, 330, 255)
            draw_text(screen, "Press ENTER to begin 30-second mixed quiz", small_font, WHITE, 290, 360)
            draw_text(screen, "After the timer, you enter the act map.", small_font, WHITE, 360, 395)
            draw_text(screen, "Created by Justin Girard", tiny_font, WHITE, 900, 670)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        header_rect = pygame.Rect(20, 18, WIDTH - 40, 96)
        pygame.draw.rect(screen, PANEL_DARK, header_rect, border_radius=14)
        pygame.draw.rect(screen, WHITE, header_rect, 2, border_radius=14)
        draw_text(screen, "Macbeth Interactive Scenes", subtitle_font, WHITE, 350, 32)
        draw_text(screen, f"Total Score: {total_score}/{len(RAPID_QUIZ) + total_scene_questions}", font, WHITE, 28, 82)
        draw_text(screen, f"Acts Completed: {len(completed_acts)}/5", font, WHITE, 840, 82)
        draw_text(screen, "Created by Justin Girard", tiny_font, WHITE, 900, 670)

        if state == "rapid_quiz":
            remaining = max(0, RAPID_TIME_SECONDS - int((pygame.time.get_ticks() - rapid_start_ms) / 1000))
            panel = pygame.Rect(120, 150, 860, 430)
            pygame.draw.rect(screen, PANEL, panel, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel, 2, border_radius=12)
            q = RAPID_QUIZ[rapid_order[rapid_idx]]
            draw_text(screen, "Rapid Mixed Quiz", subtitle_font, ACCENT, 430, 170)
            draw_text(screen, f"Time: {remaining}s", font, WHITE, 160, 170)
            draw_text(screen, f"Answered: {rapid_answered}", font, WHITE, 850, 170)
            draw_wrapped_text(screen, q["q"], font, WHITE, pygame.Rect(160, 230, 780, 80))
            for i, choice in enumerate(q["choices"], start=1):
                draw_text(screen, f"{i}) {choice}", small_font, WHITE, 190, 300 + (i - 1) * 46)
            draw_text(screen, "Press 1-4 to answer as many as you can in 30 seconds.", small_font, WHITE, 240, 500)
            if rapid_feedback:
                feedback_color = GOOD if rapid_feedback == "Correct" else BAD
                draw_text(screen, rapid_feedback, small_font, feedback_color, 470, 540)

        elif state == "map":
            draw_text(screen, "Move: WASD/Arrows | Press E to open act", font, WHITE, 320, 128)
            draw_text(screen, "Each act has a scene selection screen.", small_font, WHITE, 370, 155)
            for idx, act in enumerate(ACTS):
                base_color = ZONE_DONE if idx in completed_acts else ZONE_COLOR
                color = ZONE_HOVER if player.colliderect(act["rect"]) else base_color
                pygame.draw.rect(screen, color, act["rect"], border_radius=10)
                pygame.draw.rect(screen, BLACK, act["rect"], 2, border_radius=10)
                draw_text(screen, act["name"], font, BLACK, act["rect"].x + 54, act["rect"].y + 20)
                draw_text(screen, f"{len(act['scenes'])} scenes", tiny_font, BLACK, act["rect"].x + 52, act["rect"].y + 55)
                draw_text(screen, f"Done: {len(completed_scenes[idx])}/{len(act['scenes'])}", tiny_font, BLACK, act["rect"].x + 52, act["rect"].y + 74)
            draw_person(screen, player.centerx, player.y + 6, PLAYER_COLOR, 1.05)
            draw_text(screen, "You", small_font, WHITE, player.x - 2, player.y - 22)

        elif state == "scene_select":
            act = ACTS[selected_act_idx]
            draw_text(screen, f"{act['name']} - Scene Select", subtitle_font, WHITE, 390, 126)
            draw_text(screen, "UP/DOWN choose | ENTER play | ESC map", small_font, WHITE, 360, 160)
            panel_rect = pygame.Rect(160, 200, 780, 410)
            pygame.draw.rect(screen, PANEL, panel_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=12)
            start = max(0, selected_scene_cursor - 8)
            visible_scenes = act["scenes"][start:start + 12]
            for i, scene in enumerate(visible_scenes):
                real_idx = start + i
                y = 225 + i * 30
                marker = ">" if real_idx == selected_scene_cursor else " "
                status = " [Complete]" if real_idx in completed_scenes[selected_act_idx] else ""
                color = ACCENT if real_idx == selected_scene_cursor else WHITE
                draw_text(screen, f"{marker} {real_idx + 1}. {scene['title']}{status}", tiny_font, color, 185, y)

        elif state == "scene":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} | {scene['title']}", font, WHITE, 220, 128)
            stage_rect = pygame.Rect(120, 160, 860, 340)
            pygame.draw.rect(screen, PANEL, stage_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, stage_rect, 2, border_radius=12)
            pygame.draw.rect(screen, (70, 58, 50), pygame.Rect(140, 440, 820, 40), border_radius=8)
            unique_speakers = []
            for raw in scene["script"]:
                speaker, _ = parse_script_line(raw)
                if speaker not in unique_speakers:
                    unique_speakers.append(speaker)
            if not unique_speakers:
                unique_speakers = ["Narrator"]
            spacing = 820 // (len(unique_speakers) + 1)
            actor_positions = {}
            for idx, speaker in enumerate(unique_speakers, start=1):
                actor_positions[speaker] = (140 + spacing * idx, 345)
            palette = [(221, 117, 117), (120, 176, 240), (136, 206, 152), (224, 190, 103), (196, 145, 230)]
            for idx, speaker in enumerate(unique_speakers):
                x, y = actor_positions[speaker]
                draw_person(screen, x, y, palette[idx % len(palette)], 1.0)
                draw_text(screen, speaker, small_font, WHITE, x - 45, y + 58)
            current_line = scene["script"][scene_line_idx]
            current_speaker, spoken_text = parse_script_line(current_line)
            if current_speaker in actor_positions:
                sx, sy = actor_positions[current_speaker]
                draw_speech_bubble(screen, spoken_text, small_font, sx, sy - 10)
            draw_text(screen, "SPACE = next line", font, WHITE, 430, 560)
            draw_text(screen, f"Line {scene_line_idx + 1}/{len(scene['script'])}", small_font, WHITE, 465, 590)

        elif state == "question":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} Quiz | {scene['title']}", font, WHITE, 220, 128)
            panel_rect = pygame.Rect(120, 180, 860, 320)
            pygame.draw.rect(screen, PANEL, panel_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=12)
            statement, _ = scene["questions"][question_idx]
            draw_wrapped_text(screen, statement, font, WHITE, pygame.Rect(150, 220, 800, 160))
            draw_text(screen, "Press T for True or F for False", font, WHITE, 360, 430)
            if feedback:
                color = GOOD if feedback.startswith("Correct") else BAD
                draw_text(screen, feedback, font, color, 300, 470)

        elif state == "scene_complete":
            draw_text(screen, "Scene Complete!", subtitle_font, GOOD, 430, 215)
            draw_text(screen, last_completed_scene, font, WHITE, 210, 270)
            draw_text(screen, "Press ENTER to return.", font, WHITE, 420, 330)

        elif state == "act_complete":
            draw_text(screen, f"{last_completed_act} Complete!", subtitle_font, GOOD, 400, 215)
            draw_text(screen, "Every scene in this act is done.", font, WHITE, 400, 275)
            draw_text(screen, "Press ENTER to go back to map.", font, WHITE, 380, 335)

        elif state == "end":
            draw_text(screen, "The Full Play Is Complete!", subtitle_font, WHITE, 330, 175)
            draw_text(screen, f"Rapid Quiz: {rapid_score}/{max(1, rapid_answered)}", font, WHITE, 420, 240)
            draw_text(screen, f"Scene Quiz: {scene_score}/{total_scene_questions}", font, WHITE, 420, 280)
            draw_text(screen, "Press R to restart | Press M for map", font, WHITE, 365, 360)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
import sys
import pygame


WIDTH, HEIGHT = 1100, 700
FPS = 60
PLAYER_SPEED = 4

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
BG = (20, 23, 30)
PLAYER_COLOR = (90, 180, 255)
ZONE_COLOR = (102, 205, 149)
ZONE_HOVER = (255, 210, 90)
ZONE_DONE = (120, 130, 145)
PANEL = (48, 52, 63)
PANEL_DARK = (32, 36, 46)
GOOD = (70, 190, 110)
BAD = (210, 90, 90)
ACCENT = (188, 152, 88)


ACTS = [
    {
        "name": "Act 1",
        "rect": pygame.Rect(70, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - The Witches on the Heath", "script": ["Witch 1: When shall we three meet again, in thunder, lightning, or in rain?", "Witch 2: When the hurlyburly's done, when the battle's lost and won.", "Witch 3: That will be ere the set of sun.", "All Witches: Fair is foul, and foul is fair."], "questions": [("The witches appear before Macbeth is seen.", True), ("The witches say weather will remain peaceful.", False)]},
            {"title": "Scene 2 - Report from Battle", "script": ["Captain: For brave Macbeth, well he deserves that name.", "Duncan: O valiant cousin, worthy gentleman.", "Ross: The thane of Cawdor has betrayed us.", "Duncan: What he hath lost, noble Macbeth hath won."], "questions": [("Duncan rewards Macbeth with Cawdor's title.", True), ("Macbeth is punished for cowardice in this scene.", False)]},
            {"title": "Scene 3 - Prophecies Given", "script": ["Witch 1: All hail, Macbeth, thane of Glamis!", "Witch 2: All hail, Macbeth, thane of Cawdor!", "Witch 3: All hail, Macbeth, that shalt be king hereafter!", "Banquo: You shall get kings, though you be none."], "questions": [("The witches also predict Banquo's descendants will be kings.", True), ("Macbeth immediately rejects all ambition here.", False)]},
            {"title": "Scene 4 - Prince of Cumberland", "script": ["Duncan: Signs of nobleness, like stars, shall shine on all deservers.", "Duncan: We will establish our estate upon our eldest, Malcolm.", "Macbeth: The Prince of Cumberland! That is a step on which I must fall down, or else o'erleap.", "Macbeth: Stars, hide your fires; let not light see my black and deep desires."], "questions": [("Malcolm is named Prince of Cumberland.", True), ("Macbeth openly tells Duncan he wants the throne.", False)]},
            {"title": "Scene 5 - Lady Macbeth Reads", "script": ["Lady Macbeth: Yet do I fear thy nature; it is too full o' the milk of human kindness.", "Lady Macbeth: Come, you spirits, unsex me here.", "Messenger: The king comes here tonight.", "Lady Macbeth: Leave all the rest to me."], "questions": [("Lady Macbeth calls on spirits to harden her.", True), ("Lady Macbeth wants Macbeth to stay innocent and passive.", False)]},
            {"title": "Scene 6 - Duncan at Inverness", "script": ["Duncan: This castle hath a pleasant seat.", "Banquo: The heaven's breath smells wooingly here.", "Lady Macbeth: All our service in every point twice done and then done double.", "Duncan: Fair and noble hostess, we are your guest tonight."], "questions": [("Duncan feels safe at Macbeth's castle.", True), ("Banquo warns Duncan to leave immediately.", False)]},
            {"title": "Scene 7 - Macbeth Decides", "script": ["Macbeth: If it were done when 'tis done, then 'twere well it were done quickly.", "Macbeth: We will proceed no further in this business.", "Lady Macbeth: When you durst do it, then you were a man.", "Macbeth: I am settled, and bend up each corporal agent to this terrible feat."], "questions": [("Lady Macbeth persuades Macbeth to continue the murder plan.", True), ("Macbeth decides to confess to Duncan instead.", False)]},
        ],
    },
    {
        "name": "Act 2",
        "rect": pygame.Rect(280, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Dagger Soliloquy", "script": ["Banquo: I dreamt last night of the three weird sisters.", "Macbeth: If you shall cleave to my consent, when 'tis, it shall make honor for you.", "Macbeth: Is this a dagger which I see before me, the handle toward my hand?", "Macbeth: Thou marshall'st me the way that I was going."], "questions": [("Macbeth hallucinates a dagger before the murder.", True), ("Banquo orders Macbeth to kill Duncan.", False)]},
            {"title": "Scene 2 - Duncan Murdered", "script": ["Lady Macbeth: That which hath made them drunk hath made me bold.", "Macbeth: I have done the deed. Didst thou not hear a noise?", "Macbeth: Methought I heard a voice cry, 'Sleep no more! Macbeth does murder sleep.'", "Lady Macbeth: A little water clears us of this deed."], "questions": [("Macbeth hears imaginary voices after killing Duncan.", True), ("Lady Macbeth says they should immediately surrender.", False)]},
            {"title": "Scene 3 - The Porter and Discovery", "script": ["Porter: Knock, knock! Who's there, i' the name of Beelzebub?", "Macduff: O horror, horror, horror! Tongue nor heart cannot conceive nor name thee!", "Macbeth: Had I but died an hour before this chance, I had lived a blessed time.", "Donalbain: There's daggers in men's smiles."], "questions": [("Macduff discovers Duncan's body.", True), ("Duncan's sons decide to stay in Scotland for safety.", False)]},
            {"title": "Scene 4 - Unnatural Signs", "script": ["Old Man: By the clock 'tis day, and yet dark night strangles the traveling lamp.", "Ross: And Duncan's horses turned wild in nature.", "Macduff: Those that Macbeth hath slain.", "Ross: The heavens, as troubled with man's act, threaten his bloody stage."], "questions": [("Nature behaves strangely after Duncan's murder.", True), ("Macduff attends Macbeth's coronation at Scone.", False)]},
        ],
    },
    {
        "name": "Act 3",
        "rect": pygame.Rect(490, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Banquo Suspects Macbeth", "script": ["Banquo: Thou hast it now: king, Cawdor, Glamis, all, as the weird women promised.", "Macbeth: Ride you this afternoon?", "Macbeth: Our fears in Banquo stick deep.", "Macbeth: It is concluded. Banquo, thy soul's flight, if it find heaven, must find it out tonight."], "questions": [("Macbeth arranges Banquo's murder.", True), ("Banquo fully trusts Macbeth's rule.", False)]},
            {"title": "Scene 2 - Macbeth's Fear Deepens", "script": ["Lady Macbeth: Naught's had, all's spent, where our desire is got without content.", "Macbeth: O, full of scorpions is my mind, dear wife!", "Macbeth: Things bad begun make strong themselves by ill.", "Lady Macbeth: You must leave this."], "questions": [("Macbeth tells Lady Macbeth he is mentally tormented.", True), ("Lady Macbeth knows every detail of Banquo's ambush plan.", False)]},
            {"title": "Scene 3 - Banquo Ambushed", "script": ["First Murderer: Stand to't.", "Banquo: O treachery! Fly, good Fleance, fly, fly, fly!", "Third Murderer: Who did strike out the light?", "First Murderer: Fleance is 'scaped."], "questions": [("Fleance escapes while Banquo is killed.", True), ("Banquo kills all the murderers and survives.", False)]},
            {"title": "Scene 4 - Banquet and Ghost", "script": ["Macbeth: The table's full.", "Lennox: Here is a place reserved, sir.", "Macbeth: Thou canst not say I did it; never shake thy gory locks at me.", "Lady Macbeth: Are you a man?"], "questions": [("Macbeth sees Banquo's ghost at the banquet.", True), ("The guests can all see the ghost too.", False)]},
            {"title": "Scene 5 - Hecate's Rebuke", "script": ["Hecate: How did you dare to trade and traffic with Macbeth?", "Hecate: Security is mortals' chiefest enemy.", "Hecate: He shall spurn fate, scorn death, and bear his hopes above wisdom, grace, and fear.", "Hecate: I'll spend my time for this night."], "questions": [("Hecate plans to lure Macbeth into false confidence.", True), ("Hecate orders the witches to help Macduff.", False)]},
            {"title": "Scene 6 - Lennox and the Lord", "script": ["Lennox: Things have been strangely borne.", "Lord: The tyrant's feast has become fear.", "Lord: Macduff is gone to pray the holy king in England for aid.", "Lennox: May soon return this our suffering country under a hand accursed."], "questions": [("Macduff seeks help from England.", True), ("Lennox openly praises Macbeth as a just ruler.", False)]},
        ],
    },
    {
        "name": "Act 4",
        "rect": pygame.Rect(700, 190, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Apparitions and Warnings", "script": ["Witches: Double, double toil and trouble; fire burn and cauldron bubble.", "First Apparition: Beware Macduff.", "Second Apparition: None of woman born shall harm Macbeth.", "Third Apparition: Macbeth shall never vanquished be until Great Birnam Wood comes to Dunsinane.", "Macbeth: The firstlings of my heart shall be the firstlings of my hand."], "questions": [("The prophecies make Macbeth overconfident.", True), ("The apparitions tell Macbeth to surrender the crown.", False)]},
            {"title": "Scene 2 - Macduff's Castle Attacked", "script": ["Lady Macduff: Wisdom? to leave his wife, to leave his babes?", "Ross: I dare not speak much further.", "Messenger: Bless you, fair dame! Flee from this place.", "Murderer: What, you egg! Young fry of treachery!", "Lady Macduff: Murder!"], "questions": [("Macbeth's men kill Macduff's family.", True), ("Lady Macduff escapes safely with all her children.", False)]},
            {"title": "Scene 3 - England: Grief and Alliance", "script": ["Malcolm: This tyrant, whose sole name blisters our tongues.", "Macduff: Bleed, bleed, poor country!", "Ross: Your castle is surprised; your wife and babes savagely slaughtered.", "Macduff: All my pretty ones? Did you say all?", "Malcolm: Be this the whetstone of your sword."], "questions": [("Macduff learns his family has been murdered.", True), ("Macduff decides to forgive Macbeth and make peace.", False)]},
        ],
    },
    {
        "name": "Act 5",
        "rect": pygame.Rect(390, 330, 320, 120),
        "scenes": [
            {"title": "Scene 1 - Sleepwalking", "script": ["Doctor: I have two nights watched with you, but can perceive no truth in your report.", "Gentlewoman: Lo you, here she comes.", "Lady Macbeth: Out, damned spot! Out, I say!", "Doctor: More needs she the divine than the physician."], "questions": [("Lady Macbeth reveals guilt while sleepwalking.", True), ("The doctor successfully cures Lady Macbeth in this scene.", False)]},
            {"title": "Scene 2 - Rebel Forces Gather", "script": ["Menteith: The English power is near, led on by Malcolm.", "Caithness: Great Dunsinane he strongly fortifies.", "Angus: Now does he feel his title hang loose about him.", "All: March we on to give obedience where 'tis truly owed."], "questions": [("Scottish nobles join Malcolm against Macbeth.", True), ("The thanes think Macbeth is a stable and beloved king.", False)]},
            {"title": "Scene 3 - Macbeth at Dunsinane", "script": ["Macbeth: Bring me no more reports; let them fly all.", "Macbeth: I'll fight till from my bones my flesh be hacked.", "Doctor: Not so sick, my lord, as she is troubled with thick-coming fancies.", "Macbeth: Canst thou not minister to a mind diseased?"], "questions": [("Macbeth asks for medical help for Lady Macbeth's mind.", True), ("Macbeth plans to run away immediately.", False)]},
            {"title": "Scene 4 - Branches from Birnam", "script": ["Malcolm: Let every soldier hew him down a bough and bear't before him.", "Soldier: We shall shadow the numbers of our host.", "Siward: The time approaches.", "Malcolm: Near Birnam Wood shall we well meet them."], "questions": [("Malcolm uses tree branches to hide troop numbers.", True), ("Malcolm decides not to attack Dunsinane.", False)]},
            {"title": "Scene 5 - Tomorrow Speech", "script": ["Seyton: The queen, my lord, is dead.", "Macbeth: She should have died hereafter.", "Macbeth: Tomorrow, and tomorrow, and tomorrow, creeps in this petty pace from day to day.", "Macbeth: Life's but a walking shadow, a poor player."], "questions": [("Macbeth delivers his 'Tomorrow' soliloquy.", True), ("Macbeth celebrates joyfully at Lady Macbeth's death.", False)]},
            {"title": "Scene 6 - Battle Lines Drawn", "script": ["Malcolm: Now near enough; your leavy screens throw down.", "Siward: Make all our trumpets speak.", "Macduff: There is no boasting like a fool.", "Soldier: The castle's gently rendered."], "questions": [("Malcolm's army drops their branches before battle.", True), ("Macduff refuses to fight anyone.", False)]},
            {"title": "Scene 7 - Young Siward and Macbeth", "script": ["Young Siward: What is thy name?", "Macbeth: Thou'lt be afraid to hear it.", "Young Siward: No, though thou call'st thyself a hotter name than any is in hell.", "Macbeth: My name's Macbeth.", "Young Siward: The devil himself could not pronounce a title more hateful to mine ear."], "questions": [("Macbeth kills Young Siward.", True), ("Young Siward defeats Macbeth here.", False)]},
            {"title": "Scene 8 - Macduff's Challenge", "script": ["Macduff: Turn, hell-hound, turn!", "Macbeth: I bear a charmed life, which must not yield to one of woman born.", "Macduff: Macduff was from his mother's womb untimely ripped.", "Macbeth: I'll not fight with thee.", "Macduff: Then yield thee, coward."], "questions": [("Macduff reveals he was not born in the usual way.", True), ("Macbeth surrenders peacefully and survives.", False)]},
        ],
    },
]


def parse_script_line(line):
    if ":" in line:
        speaker, text = line.split(":", 1)
        return speaker.strip(), text.strip()
    return "Narrator", line


def draw_person(surface, x, y, body_color, scale=1.0):
    head_radius = int(10 * scale)
    body_len = int(24 * scale)
    arm_len = int(14 * scale)
    leg_len = int(18 * scale)

    pygame.draw.circle(surface, body_color, (x, y), head_radius)
    pygame.draw.line(surface, body_color, (x, y + head_radius), (x, y + head_radius + body_len), 3)
    pygame.draw.line(surface, body_color, (x - arm_len, y + head_radius + 8), (x + arm_len, y + head_radius + 8), 3)
    pygame.draw.line(surface, body_color, (x, y + head_radius + body_len), (x - leg_len // 2, y + head_radius + body_len + leg_len), 3)
    pygame.draw.line(surface, body_color, (x, y + head_radius + body_len), (x + leg_len // 2, y + head_radius + body_len + leg_len), 3)


def draw_speech_bubble(surface, text, font, x, y):
    bubble_rect = pygame.Rect(x - 170, y - 78, 340, 62)
    pygame.draw.rect(surface, WHITE, bubble_rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, bubble_rect, 2, border_radius=10)
    pygame.draw.polygon(surface, WHITE, [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)])
    pygame.draw.polygon(surface, BLACK, [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)], 2)
    draw_wrapped_text(surface, text, font, BLACK, bubble_rect, line_spacing=2)


def draw_text(surface, text, font, color, x, y):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=6):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= rect.width - 10:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)

    y = rect.y + 8
    for line in lines:
        img = font.render(line.strip(), True, color)
        surface.blit(img, (rect.x + 8, y))
        y += font.get_height() + line_spacing


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Macbeth Walkthrough Quiz Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("georgia", 58, bold=True)
    subtitle_font = pygame.font.SysFont("georgia", 28, bold=True)
    font = pygame.font.SysFont("cambria", 24)
    small_font = pygame.font.SysFont("cambria", 20)
    tiny_font = pygame.font.SysFont("cambria", 18)

    player = pygame.Rect(100, 560, 30, 30)
    score = 0
    total_questions = sum(len(scene["questions"]) for act in ACTS for scene in act["scenes"])

    state = "title"
    selected_act_idx = None
    selected_scene_idx = 0
    selected_scene_cursor = 0
    scene_line_idx = 0
    question_idx = 0
    feedback = ""
    completed_acts = set()
    last_completed_act = ""
    last_completed_scene = ""
    completed_scenes = {i: set() for i in range(len(ACTS))}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "title":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        state = "map"
                elif state == "map":
                    if event.key == pygame.K_e:
                        for idx, act in enumerate(ACTS):
                            if player.colliderect(act["rect"]):
                                selected_act_idx = idx
                                selected_scene_cursor = 0
                                state = "scene_select"
                                break
                elif state == "scene_select":
                    act = ACTS[selected_act_idx]
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_scene_cursor = (selected_scene_cursor - 1) % len(act["scenes"])
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_scene_cursor = (selected_scene_cursor + 1) % len(act["scenes"])
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected_scene_idx = selected_scene_cursor
                        scene_line_idx = 0
                        question_idx = 0
                        feedback = ""
                        state = "scene"
                    elif event.key == pygame.K_ESCAPE:
                        selected_act_idx = None
                        state = "map"
                elif state == "scene":
                    if event.key == pygame.K_SPACE:
                        act = ACTS[selected_act_idx]
                        scene = act["scenes"][selected_scene_idx]
                        scene_line_idx += 1
                        if scene_line_idx >= len(scene["script"]):
                            scene_line_idx = len(scene["script"]) - 1
                            question_idx = 0
                            feedback = ""
                            state = "question"
                elif state == "question":
                    if event.key in (pygame.K_t, pygame.K_f):
                        act = ACTS[selected_act_idx]
                        scene = act["scenes"][selected_scene_idx]
                        _, answer = scene["questions"][question_idx]
                        user_answer = event.key == pygame.K_t
                        if user_answer == answer:
                            score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong. Correct answer: {'True' if answer else 'False'}"

                        question_idx += 1
                        if question_idx >= len(scene["questions"]):
                            completed_scenes[selected_act_idx].add(selected_scene_idx)
                            last_completed_scene = scene["title"]
                            if len(completed_scenes[selected_act_idx]) == len(act["scenes"]):
                                completed_acts.add(selected_act_idx)
                                last_completed_act = act["name"]
                            state = "scene_complete"
                elif state == "scene_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if len(completed_acts) == len(ACTS):
                            state = "end"
                        elif selected_act_idx in completed_acts:
                            state = "act_complete"
                        else:
                            state = "scene_select"
                elif state == "act_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_m):
                        selected_act_idx = None
                        state = "map"
                elif state == "end":
                    if event.key == pygame.K_r:
                        score = 0
                        selected_act_idx = None
                        selected_scene_idx = 0
                        selected_scene_cursor = 0
                        scene_line_idx = 0
                        question_idx = 0
                        feedback = ""
                        completed_acts = set()
                        last_completed_act = ""
                        last_completed_scene = ""
                        completed_scenes = {i: set() for i in range(len(ACTS))}
                        state = "title"
                        player.topleft = (100, 560)
                    elif event.key == pygame.K_m:
                        selected_act_idx = None
                        state = "map"

        keys = pygame.key.get_pressed()
        if state == "map":
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED
            player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        screen.fill(BG)

        if state == "title":
            title_panel = pygame.Rect(130, 120, 840, 430)
            pygame.draw.rect(screen, PANEL_DARK, title_panel, border_radius=18)
            pygame.draw.rect(screen, ACCENT, title_panel, 3, border_radius=18)
            draw_text(screen, "MACBETH", title_font, WHITE, 380, 170)
            draw_text(screen, "Interactive Scene Journey", subtitle_font, ACCENT, 330, 255)
            draw_text(screen, "Press ENTER to Start", subtitle_font, WHITE, 365, 360)
            draw_text(screen, "Walk through each act, choose scenes, and answer True/False questions.", small_font, WHITE, 225, 430)
            draw_text(screen, "Created by Justin Girard", tiny_font, WHITE, 900, 670)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        header_rect = pygame.Rect(20, 18, WIDTH - 40, 96)
        pygame.draw.rect(screen, PANEL_DARK, header_rect, border_radius=14)
        pygame.draw.rect(screen, WHITE, header_rect, 2, border_radius=14)
        draw_text(screen, "Macbeth Interactive Scenes", subtitle_font, WHITE, 350, 32)
        draw_text(screen, f"Score: {score}/{total_questions}", font, WHITE, 28, 82)
        draw_text(screen, f"Acts Completed: {len(completed_acts)}/5", font, WHITE, 840, 82)
        draw_text(screen, "Created by Justin Girard", tiny_font, WHITE, 900, 670)

        if state == "map":
            draw_text(screen, "Move: WASD/Arrows | Press E to open act", font, WHITE, 320, 128)
            draw_text(screen, "Each act now has a dedicated scene selection screen.", small_font, WHITE, 305, 155)

            for idx, act in enumerate(ACTS):
                base_color = ZONE_DONE if idx in completed_acts else ZONE_COLOR
                color = ZONE_HOVER if player.colliderect(act["rect"]) else base_color
                pygame.draw.rect(screen, color, act["rect"], border_radius=10)
                pygame.draw.rect(screen, BLACK, act["rect"], 2, border_radius=10)
                draw_text(screen, act["name"], font, BLACK, act["rect"].x + 54, act["rect"].y + 20)
                draw_text(screen, f"{len(act['scenes'])} scenes", tiny_font, BLACK, act["rect"].x + 52, act["rect"].y + 55)
                draw_text(screen, f"Done: {len(completed_scenes[idx])}/{len(act['scenes'])}", tiny_font, BLACK, act["rect"].x + 52, act["rect"].y + 74)
                if idx in completed_acts:
                    draw_text(screen, "COMPLETE", tiny_font, GOOD, act["rect"].x + 120, act["rect"].y + 74)

            draw_person(screen, player.centerx, player.y + 6, PLAYER_COLOR, 1.05)
            draw_text(screen, "You", small_font, WHITE, player.x - 2, player.y - 22)

        elif state == "scene_select":
            act = ACTS[selected_act_idx]
            draw_text(screen, f"{act['name']} - Scene Select", subtitle_font, WHITE, 390, 126)
            draw_text(screen, "UP/DOWN to choose, ENTER to play, ESC to map", small_font, WHITE, 320, 160)
            panel_rect = pygame.Rect(160, 200, 780, 410)
            pygame.draw.rect(screen, PANEL, panel_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=12)

            start = max(0, selected_scene_cursor - 8)
            visible_scenes = act["scenes"][start:start + 12]
            for i, scene in enumerate(visible_scenes):
                real_idx = start + i
                y = 225 + i * 30
                marker = ">" if real_idx == selected_scene_cursor else " "
                status = " [Complete]" if real_idx in completed_scenes[selected_act_idx] else ""
                color = ACCENT if real_idx == selected_scene_cursor else WHITE
                draw_text(screen, f"{marker} {real_idx + 1}. {scene['title']}{status}", tiny_font, color, 185, y)

        elif state == "scene":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} | {scene['title']}", font, WHITE, 220, 128)
            stage_rect = pygame.Rect(120, 160, 860, 340)
            pygame.draw.rect(screen, PANEL, stage_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, stage_rect, 2, border_radius=12)
            pygame.draw.rect(screen, (70, 58, 50), pygame.Rect(140, 440, 820, 40), border_radius=8)

            unique_speakers = []
            for raw in scene["script"]:
                speaker, _ = parse_script_line(raw)
                if speaker not in unique_speakers:
                    unique_speakers.append(speaker)
            if not unique_speakers:
                unique_speakers = ["Narrator"]

            spacing = 820 // (len(unique_speakers) + 1)
            actor_positions = {}
            for idx, speaker in enumerate(unique_speakers, start=1):
                actor_positions[speaker] = (140 + spacing * idx, 345)

            palette = [(221, 117, 117), (120, 176, 240), (136, 206, 152), (224, 190, 103), (196, 145, 230)]
            for idx, speaker in enumerate(unique_speakers):
                x, y = actor_positions[speaker]
                draw_person(screen, x, y, palette[idx % len(palette)], 1.0)
                draw_text(screen, speaker, small_font, WHITE, x - 45, y + 58)

            current_line = scene["script"][scene_line_idx]
            current_speaker, spoken_text = parse_script_line(current_line)
            if current_speaker in actor_positions:
                sx, sy = actor_positions[current_speaker]
                draw_speech_bubble(screen, spoken_text, small_font, sx, sy - 10)
                draw_text(screen, f"Speaking: {current_speaker}", font, WHITE, 435, 520)
            else:
                draw_text(screen, current_line, font, WHITE, 250, 520)

            draw_text(screen, "SPACE = next line", font, WHITE, 430, 560)
            draw_text(screen, f"Line {scene_line_idx + 1}/{len(scene['script'])}", small_font, WHITE, 465, 590)

        elif state == "question":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} Quiz | {scene['title']}", font, WHITE, 220, 128)
            panel_rect = pygame.Rect(120, 180, 860, 320)
            pygame.draw.rect(screen, PANEL, panel_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=12)

            statement, _ = scene["questions"][question_idx]
            draw_wrapped_text(screen, statement, font, WHITE, pygame.Rect(150, 220, 800, 160))
            draw_text(screen, "Press T for True or F for False", font, WHITE, 360, 430)
            if feedback:
                color = GOOD if feedback.startswith("Correct") else BAD
                draw_text(screen, feedback, font, color, 300, 470)
            draw_text(screen, f"Question {question_idx + 1}/{len(scene['questions'])}", small_font, WHITE, 465, 515)

        elif state == "scene_complete":
            draw_text(screen, "Scene Complete!", subtitle_font, GOOD, 430, 215)
            draw_text(screen, last_completed_scene, font, WHITE, 210, 270)
            draw_text(screen, "Press ENTER to return.", font, WHITE, 420, 330)
            draw_text(screen, "You were kicked out after finishing the scene.", small_font, WHITE, 330, 380)

        elif state == "act_complete":
            draw_text(screen, f"{last_completed_act} Complete!", subtitle_font, GOOD, 400, 215)
            draw_text(screen, "Every scene in this act is done.", font, WHITE, 400, 275)
            draw_text(screen, "Press ENTER to go back to map.", font, WHITE, 380, 335)

        elif state == "end":
            draw_text(screen, "The Full Play Is Complete!", subtitle_font, WHITE, 330, 175)
            draw_text(screen, f"Final Score: {score}/{total_questions}", font, WHITE, 435, 250)
            draw_text(screen, "You completed every individual scene in Macbeth.", font, WHITE, 315, 305)
            draw_text(screen, "Press R to restart | Press M for map", font, WHITE, 365, 360)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
import sys
import pygame


WIDTH, HEIGHT = 1100, 700
FPS = 60
PLAYER_SPEED = 4

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
BG = (22, 25, 34)
PLAYER_COLOR = (90, 180, 255)
ZONE_COLOR = (102, 205, 149)
ZONE_HOVER = (255, 210, 90)
ZONE_DONE = (120, 130, 145)
PANEL = (48, 52, 63)
PANEL_DARK = (36, 40, 52)
GOOD = (70, 190, 110)
BAD = (210, 90, 90)


ACTS = [
    {
        "name": "Act 1",
        "rect": pygame.Rect(70, 170, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Thunder and Witches", "script": ["Witch: Fair is foul, and foul is fair."], "questions": [("Act 1 Scene 1 introduces the witches.", True)]},
            {"title": "Scene 2 - The Battle Report", "script": ["Captain: Brave Macbeth has won the field.", "Duncan: He is worthy of honor."], "questions": [("King Duncan praises Macbeth here.", True)]},
            {"title": "Scene 3 - First Prophecies", "script": ["Witch: All hail Macbeth, future king.", "Banquo: What of me?", "Witch: Thou shalt father kings."], "questions": [("The witches predict Banquo's line of kings.", True)]},
            {"title": "Scene 4 - Prince of Cumberland", "script": ["Duncan: Malcolm shall be Prince of Cumberland.", "Macbeth: A step that blocks my way."], "questions": [("Macbeth feels threatened by Malcolm's title.", True)]},
            {"title": "Scene 5 - Lady Macbeth Plots", "script": ["Lady Macbeth: Your nature is too full of kindness.", "Lady Macbeth: We must hide our darkest intent."], "questions": [("Lady Macbeth pushes Macbeth toward murder.", True)]},
            {"title": "Scene 6 - Duncan Arrives at Inverness", "script": ["Duncan: This castle has a pleasant seat.", "Lady Macbeth: Welcome, my gracious lord."], "questions": [("Duncan suspects danger at once.", False)]},
            {"title": "Scene 7 - Macbeth's Doubt", "script": ["Macbeth: We will proceed no further in this business.", "Lady Macbeth: Screw your courage to the sticking place."], "questions": [("Macbeth first tries to refuse the murder plan.", True)]},
        ],
    },
    {
        "name": "Act 2",
        "rect": pygame.Rect(280, 170, 190, 100),
        "scenes": [
            {"title": "Scene 1 - The Dagger Vision", "script": ["Banquo: We dreamed of the weird sisters.", "Macbeth: Is this a dagger I see before me?"], "questions": [("Macbeth sees a vision of a dagger.", True)]},
            {"title": "Scene 2 - Duncan's Murder", "script": ["Lady Macbeth: Did you not hear a noise?", "Macbeth: I have done the deed."], "questions": [("Macbeth kills Duncan offstage in this scene.", True)]},
            {"title": "Scene 3 - The Discovery", "script": ["Porter: Knock, knock!", "Macduff: O horror! The king is murdered."], "questions": [("Macduff discovers Duncan's body.", True)]},
            {"title": "Scene 4 - Fear in Scotland", "script": ["Ross: Strange things fill the day with darkness.", "Old Man: Nature is disturbed."], "questions": [("This scene shows order returning to normal.", False)]},
        ],
    },
    {
        "name": "Act 3",
        "rect": pygame.Rect(490, 170, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Banquo in Danger", "script": ["Banquo: I fear you played most foully for the crown.", "Macbeth: Banquo must be removed."], "questions": [("Macbeth hires murderers against Banquo.", True)]},
            {"title": "Scene 2 - Dark Thoughts", "script": ["Lady Macbeth: What's done is done.", "Macbeth: We have scorched the snake, not killed it."], "questions": [("Macbeth feels fully safe and peaceful now.", False)]},
            {"title": "Scene 3 - The Ambush", "script": ["Murderer: Banquo is dead.", "Murderer: Fleance has escaped."], "questions": [("Fleance escapes the murderers.", True)]},
            {"title": "Scene 4 - The Banquet Ghost", "script": ["Macbeth: Which of you have done this?", "Lords: The king is troubled."], "questions": [("Macbeth sees Banquo's ghost at dinner.", True)]},
            {"title": "Scene 5 - Hecate's Plan", "script": ["Hecate: Macbeth shall be led into deeper confusion."], "questions": [("Hecate plans to mislead Macbeth further.", True)]},
            {"title": "Scene 6 - Resistance Grows", "script": ["Lennox: Men whisper that Macbeth rules by fear.", "Lord: Macduff has gone to England."], "questions": [("Macduff stays loyal to Macbeth here.", False)]},
        ],
    },
    {
        "name": "Act 4",
        "rect": pygame.Rect(700, 170, 190, 100),
        "scenes": [
            {"title": "Scene 1 - Apparitions", "script": ["Witches: Double, double toil and trouble.", "Apparition: Beware Macduff.", "Apparition: None of woman born shall harm Macbeth."], "questions": [("The apparitions make Macbeth overconfident.", True)]},
            {"title": "Scene 2 - Macduff's Family", "script": ["Lady Macduff: He loves us not.", "Messenger: Flee, danger comes!", "Murderer: You are all marked."], "questions": [("Macbeth's men kill Macduff's household.", True)]},
            {"title": "Scene 3 - England and Resolve", "script": ["Malcolm: Let us test each other's loyalty.", "Macduff: All my pretty ones? Did you say all?"], "questions": [("Macduff vows revenge after hearing of his family.", True)]},
        ],
    },
    {
        "name": "Act 5",
        "rect": pygame.Rect(390, 320, 320, 120),
        "scenes": [
            {"title": "Scene 1 - Lady Macbeth Sleepwalks", "script": ["Doctor: She rubs her hands in her sleep.", "Lady Macbeth: Out, damned spot!"], "questions": [("Lady Macbeth shows guilt in this scene.", True)]},
            {"title": "Scene 2 - Rebels Gather", "script": ["Menteith: The English force advances.", "Caithness: We march against Macbeth."], "questions": [("Scottish nobles gather against Macbeth.", True)]},
            {"title": "Scene 3 - Macbeth Defiant", "script": ["Macbeth: Till Birnam Wood comes to Dunsinane, I cannot fear.", "Servant: The army is near, my lord."], "questions": [("Macbeth trusts the prophecy too much.", True)]},
            {"title": "Scene 4 - Branches of Birnam", "script": ["Malcolm: Let every soldier cut down a bough.", "Soldier: We hide our numbers."], "questions": [("The army uses branches as camouflage.", True)]},
            {"title": "Scene 5 - Tomorrow Soliloquy", "script": ["Seyton: The queen, my lord, is dead.", "Macbeth: Tomorrow, and tomorrow, and tomorrow..."], "questions": [("Macbeth gives a famous speech on life's meaninglessness.", True)]},
            {"title": "Scene 6 - Attack Begins", "script": ["Macduff: Make all our trumpets speak.", "Malcolm: Set on!"], "questions": [("The final attack on Dunsinane starts here.", True)]},
            {"title": "Scene 7 - Young Siward Falls", "script": ["Young Siward: What is thy name?", "Macbeth: My name's Macbeth."], "questions": [("Macbeth kills Young Siward in battle.", True)]},
            {"title": "Scene 8 - Macbeth vs Macduff", "script": ["Macbeth: I bear a charmed life.", "Macduff: I was from my mother's womb untimely ripped."], "questions": [("Macduff was not 'born of woman' in the ordinary way.", True)]},
            {"title": "Scene 9 - Victory and Order", "script": ["Malcolm: Hail, King of Scotland!", "Ross: Macduff has slain Macbeth."], "questions": [("Malcolm is restored as king in the end.", True)]},
            {"title": "Scene 10 - Honors Restored", "script": ["Malcolm: We shall call our thanes to earls.", "Lords: Hail, King Malcolm!"], "questions": [("Malcolm promises to restore order.", True)]},
            {"title": "Scene 11 - Closing Procession", "script": ["All: Peace returns to Scotland.", "Narrator: The tragedy is complete."], "questions": [("The play ends in total chaos with no ruler.", False)]},
        ],
    },
]


def parse_script_line(line):
    if ":" in line:
        speaker, text = line.split(":", 1)
        return speaker.strip(), text.strip()
    return "Narrator", line


def draw_person(surface, x, y, body_color, scale=1.0):
    head_radius = int(10 * scale)
    body_len = int(24 * scale)
    arm_len = int(14 * scale)
    leg_len = int(18 * scale)

    pygame.draw.circle(surface, body_color, (x, y), head_radius)
    pygame.draw.line(surface, body_color, (x, y + head_radius), (x, y + head_radius + body_len), 3)
    pygame.draw.line(
        surface,
        body_color,
        (x - arm_len, y + head_radius + 8),
        (x + arm_len, y + head_radius + 8),
        3,
    )
    pygame.draw.line(
        surface,
        body_color,
        (x, y + head_radius + body_len),
        (x - leg_len // 2, y + head_radius + body_len + leg_len),
        3,
    )
    pygame.draw.line(
        surface,
        body_color,
        (x, y + head_radius + body_len),
        (x + leg_len // 2, y + head_radius + body_len + leg_len),
        3,
    )


def draw_speech_bubble(surface, text, font, x, y):
    bubble_rect = pygame.Rect(x - 170, y - 78, 340, 62)
    pygame.draw.rect(surface, WHITE, bubble_rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, bubble_rect, 2, border_radius=10)
    pygame.draw.polygon(
        surface,
        WHITE,
        [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)],
    )
    pygame.draw.polygon(
        surface,
        BLACK,
        [(x - 10, y - 16), (x + 10, y - 16), (x, y - 2)],
        2,
    )
    draw_wrapped_text(surface, text, font, BLACK, bubble_rect, line_spacing=2)


def draw_text(surface, text, font, color, x, y):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=6):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= rect.width - 10:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)

    y = rect.y + 8
    for line in lines:
        img = font.render(line.strip(), True, color)
        surface.blit(img, (rect.x + 8, y))
        y += font.get_height() + line_spacing


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Macbeth Walkthrough Quiz Game")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 38, bold=True)
    font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 20)
    tiny_font = pygame.font.SysFont("arial", 18)

    player = pygame.Rect(100, 560, 30, 30)
    score = 0
    total_questions = sum(len(scene["questions"]) for act in ACTS for scene in act["scenes"])

    state = "map"  # map, scene, question, act_complete, end
    selected_act_idx = None
    selected_scene_idx = 0
    scene_line_idx = 0
    question_idx = 0
    feedback = ""
    completed_acts = set()
    last_completed_act = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "map":
                    if event.key == pygame.K_e:
                        for idx, act in enumerate(ACTS):
                            if player.colliderect(act["rect"]):
                                selected_act_idx = idx
                                selected_scene_idx = 0
                                scene_line_idx = 0
                                question_idx = 0
                                feedback = ""
                                state = "scene"
                                break
                elif state == "scene":
                    if event.key == pygame.K_SPACE:
                        act = ACTS[selected_act_idx]
                        scene = act["scenes"][selected_scene_idx]
                        scene_line_idx += 1
                        if scene_line_idx >= len(scene["script"]):
                            scene_line_idx = len(scene["script"]) - 1
                            question_idx = 0
                            feedback = ""
                            state = "question"
                elif state == "question":
                    if event.key in (pygame.K_t, pygame.K_f):
                        act = ACTS[selected_act_idx]
                        scene = act["scenes"][selected_scene_idx]
                        statement, answer = scene["questions"][question_idx]
                        user_answer = event.key == pygame.K_t
                        if user_answer == answer:
                            score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong. Correct answer: {'True' if answer else 'False'}"

                        question_idx += 1
                        if question_idx >= len(scene["questions"]):
                            selected_scene_idx += 1
                            if selected_scene_idx >= len(act["scenes"]):
                                completed_acts.add(selected_act_idx)
                                last_completed_act = act["name"]
                                selected_act_idx = None
                                selected_scene_idx = 0
                                scene_line_idx = 0
                                question_idx = 0
                                feedback = ""
                                if len(completed_acts) == len(ACTS):
                                    state = "end"
                                else:
                                    state = "act_complete"
                            else:
                                scene_line_idx = 0
                                question_idx = 0
                                feedback = ""
                                state = "scene"
                elif state == "act_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_m):
                        state = "map"
                elif state == "end":
                    if event.key == pygame.K_r:
                        score = 0
                        selected_act_idx = None
                        selected_scene_idx = 0
                        scene_line_idx = 0
                        question_idx = 0
                        feedback = ""
                        completed_acts = set()
                        last_completed_act = ""
                        state = "map"
                        player.topleft = (100, 560)
                    elif event.key == pygame.K_m:
                        state = "map"

        keys = pygame.key.get_pressed()
        if state == "map":
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED
            player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        screen.fill(BG)
        header_rect = pygame.Rect(20, 18, WIDTH - 40, 96)
        pygame.draw.rect(screen, PANEL_DARK, header_rect, border_radius=14)
        pygame.draw.rect(screen, WHITE, header_rect, 2, border_radius=14)
        draw_text(screen, "Macbeth Interactive Scenes", title_font, WHITE, 320, 30)
        draw_text(screen, f"Score: {score}/{total_questions}", font, WHITE, 28, 82)
        draw_text(screen, f"Acts Completed: {len(completed_acts)}/5", font, WHITE, 840, 82)

        if state == "map":
            draw_text(screen, "Move: WASD/Arrows | Press E to enter an act", font, WHITE, 300, 128)
            draw_text(screen, "Each act contains every scene from Macbeth.", small_font, WHITE, 380, 155)

            for idx, act in enumerate(ACTS):
                base_color = ZONE_DONE if idx in completed_acts else ZONE_COLOR
                color = ZONE_HOVER if player.colliderect(act["rect"]) else base_color
                pygame.draw.rect(screen, color, act["rect"], border_radius=10)
                pygame.draw.rect(screen, BLACK, act["rect"], 2, border_radius=10)
                draw_text(screen, act["name"], font, BLACK, act["rect"].x + 54, act["rect"].y + 20)
                draw_text(screen, f"{len(act['scenes'])} scenes", tiny_font, BLACK, act["rect"].x + 52, act["rect"].y + 55)
                if idx in completed_acts:
                    draw_text(screen, "COMPLETE", tiny_font, GOOD, act["rect"].x + 53, act["rect"].y + 75)

            draw_person(screen, player.centerx, player.y + 6, PLAYER_COLOR, 1.05)
            draw_text(screen, "You", small_font, WHITE, player.x - 2, player.y - 22)

        elif state == "scene":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} | {scene['title']}", font, WHITE, 290, 128)
            stage_rect = pygame.Rect(120, 160, 860, 340)
            pygame.draw.rect(screen, PANEL, stage_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, stage_rect, 2, border_radius=12)
            pygame.draw.rect(screen, (70, 58, 50), pygame.Rect(140, 440, 820, 40), border_radius=8)

            unique_speakers = []
            for raw in scene["script"]:
                speaker, _ = parse_script_line(raw)
                if speaker not in unique_speakers:
                    unique_speakers.append(speaker)
            if not unique_speakers:
                unique_speakers = ["Narrator"]

            spacing = 820 // (len(unique_speakers) + 1)
            actor_positions = {}
            for idx, speaker in enumerate(unique_speakers, start=1):
                actor_positions[speaker] = (140 + spacing * idx, 345)

            palette = [(221, 117, 117), (120, 176, 240), (136, 206, 152), (224, 190, 103), (196, 145, 230)]
            for idx, speaker in enumerate(unique_speakers):
                x, y = actor_positions[speaker]
                draw_person(screen, x, y, palette[idx % len(palette)], 1.0)
                draw_text(screen, speaker, small_font, WHITE, x - 45, y + 58)

            current_line = scene["script"][scene_line_idx]
            current_speaker, spoken_text = parse_script_line(current_line)
            if current_speaker in actor_positions:
                sx, sy = actor_positions[current_speaker]
                draw_speech_bubble(screen, spoken_text, small_font, sx, sy - 10)
                draw_text(screen, f"Speaking: {current_speaker}", font, WHITE, 435, 520)
            else:
                draw_text(screen, current_line, font, WHITE, 250, 520)

            draw_text(screen, "SPACE = next line", font, WHITE, 430, 560)
            draw_text(screen, f"Scene {selected_scene_idx + 1}/{len(act['scenes'])}", small_font, WHITE, 450, 590)

        elif state == "question":
            act = ACTS[selected_act_idx]
            scene = act["scenes"][selected_scene_idx]
            draw_text(screen, f"{act['name']} Quiz | {scene['title']}", font, WHITE, 270, 128)
            panel_rect = pygame.Rect(120, 180, 860, 320)
            pygame.draw.rect(screen, PANEL, panel_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, panel_rect, 2, border_radius=12)

            statement, _ = scene["questions"][question_idx]
            draw_wrapped_text(screen, statement, font, WHITE, pygame.Rect(150, 220, 800, 160))
            draw_text(screen, "Press T for True or F for False", font, WHITE, 360, 430)
            if feedback:
                color = GOOD if feedback.startswith("Correct") else BAD
                draw_text(screen, feedback, font, color, 300, 470)
            draw_text(screen, f"Question {question_idx + 1}/{len(scene['questions'])}", small_font, WHITE, 465, 515)

        elif state == "act_complete":
            draw_text(screen, f"{last_completed_act} Complete!", title_font, GOOD, 395, 210)
            draw_text(screen, "You were kicked back to the map.", font, WHITE, 390, 280)
            draw_text(screen, "Press ENTER, SPACE, or M to return.", font, WHITE, 345, 330)
            draw_text(screen, "You can now choose any remaining act.", small_font, WHITE, 390, 380)

        elif state == "end":
            draw_text(screen, "The Play Is Complete!", title_font, WHITE, 345, 170)
            draw_text(screen, f"Final Score: {score}/{total_questions}", font, WHITE, 438, 250)
            draw_text(screen, "All scenes in all 5 acts are completed.", font, WHITE, 345, 305)
            draw_text(screen, "Press R to restart everything", font, WHITE, 395, 350)
            draw_text(screen, "Press M to go back to map", font, WHITE, 420, 390)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
