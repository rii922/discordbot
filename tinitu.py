import copy
import random
import asyncio

def is_winning_hand(hand, meld=4, eye=1):
    if meld == 0 and eye == 0:
        return True
    if meld > 0:
        for i in range(9):
            if hand[i] >= 3:
                nhand = copy.copy(hand)
                nhand[i] -= 3
                if is_winning_hand(nhand, meld-1, eye):
                    return True
        for i in range(7):
            if hand[i] >= 1 and hand[i+1] >= 1 and hand[i+2] >= 1:
                nhand = copy.copy(hand)
                nhand[i] -= 1
                nhand[i+1] -= 1
                nhand[i+2] -= 1
                if is_winning_hand(nhand, meld-1, eye):
                    return True
    if eye > 0:
        for i in range(9):
            if hand[i] >= 2:
                nhand = copy.copy(hand)
                nhand[i] -= 2
                if is_winning_hand(nhand, meld, eye-1):
                    return True
    return False

def add_random_chow(hand):
    chow_list = []
    for i in range(7):
        if hand[i] <= 3 and hand[i+1] <= 3 and hand[i+2] <= 3:
            chow_list.append(i)
    chow_begin = random.choice(chow_list)
    for i in range(3):
        hand[chow_begin+i] += 1

def add_random_pong(hand):
    pong_list = []
    for i in range(9):
        if hand[i] <= 1:
            pong_list.append(i)
    pong = random.choice(pong_list)
    hand[pong] += 3

def add_random_eye(hand):
    eye_list = []
    for i in range(9):
        if hand[i] <= 2:
            eye_list.append(i)
    eye = random.choice(eye_list)
    hand[eye] += 2

def generate_quiz():
    hand = [0 for _ in range(9)]
    for _ in range(4):
        if random.randrange(4) == 0:
            add_random_pong(hand)
        else:
            add_random_chow(hand)
    add_random_eye(hand)
    eliminate_list = []
    for i in range(9):
        if hand[i] > 0:
            eliminate_list.append(i)
    hand[random.choice(eliminate_list)] -= 1
    ans = set()
    for i in range(9):
        if hand[i] <= 3:
            nhand = copy.copy(hand)
            nhand[i] += 1
            if is_winning_hand(nhand):
                ans.add(i)
    return (hand, ans)

async def play(client, message):
    hand, ans = generate_quiz()
    hand_list = []
    for i in range(9):
        hand_list += [str(i+1) for _ in range(hand[i])]
    hand_str = " ".join(hand_list)
    random.shuffle(hand_list)
    hand_str_shuffled = " ".join(hand_list)
    ans_list = [str(wait+1) for wait in ans]
    ans_list.sort()
    await message.channel.send("__**清一色何待ちクイズ**__\nこの清一色、何待ち？\n**" + hand_str_shuffled + "**")
    def check(ans_message):
        if ans_message.channel != message.channel:
            return False
        user_ans = set()
        for i in range(9):
            if str(i+1) in ans_message.content:
                user_ans.add(i)
        return user_ans == ans
    async def send_correct_message(ans_message):
        await ans_message.channel.send(ans_message.author.mention + "正解！(**" + ", ".join(ans_list) + "**待ち)")
        await ans_message.add_reaction("👍")
    try:
        ans_message = await client.wait_for("message", check=check, timeout=30)
        await send_correct_message(ans_message)
    except asyncio.TimeoutError:
        await message.channel.send("分からない？...じゃあ理牌してあげる～\n**" + hand_str + "**")
        try:
            ans_message = await client.wait_for("message", check=check, timeout=30)
            await send_correct_message(ans_message)
        except asyncio.TimeoutError:
            await message.channel.send("まだ分からない？しょうがないなあ...この待ちは**" + str(len(ans)) + "**種あるよ～")
            try:
                ans_message = await client.wait_for("message", check=check, timeout=30)
                await send_correct_message(ans_message)
            except asyncio.TimeoutError:
                await message.channel.send("残念...時間切れだよ！\n正解は**" + ", ".join(ans_list) + "**待ちでした！難しかったかな？")