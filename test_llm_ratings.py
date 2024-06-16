import csv
import json
import math
import random
import requests
import time

# Define the CSV file path and header
csv_file_path = 'ragebait_scores.csv'
header = ['Headline', 'Human Rating']

formats = [
    ('Rate whether this headline elicits anger on a scale 1-10.'
     ' 1 means no anger.  10 means lots of anger. "%s"'
     ' Reply with a single number.'),
    '''Examples:

headline:"California man sentenced to 40 years to life for fatal freeway shooting of 6-year-old boy during road rage incident"
response:9

headline:"Iran launched dozens of drones toward Israel - report"
response:1

headline:"A gang of Robber crabs invade a family picnic in Australia"
response:1


Fill in the next headline's rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don't have enough info, respond with "0"

headline:"%s"
response:''',
    '''Rate how much this headline is taking pleasure at something bad happening to someone on a scale 1-9. Your reply should be 1 character long. Reply "1" if not sure.'

headline: "%s"''',
    'On a scale 1-10, how ragebaity is this headline?  "%s".  Reply with a single number only.',
    'Rate whether this headline is trying to elicit specifically anger on a scale 1-10? "%s" Reply with a single number only.',
]


# Load human ratings from CSV file
human_ratings = []
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        headline, rating = row
        human_ratings.append((headline.strip(), int(rating)))

def make_prompt_format1():
    return formats

def make_prompt_format():
    def make_format_helper(samples):
        template = ['Examples:\n']
        for headline, rating in samples:
            headline = headline.replace('%', '%%')
            template.append('headline:"%s"\nresponse:%d\n' % (headline, rating))
        instruction = 'Fill in the next headline\'s rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don\'t have enough info, respond with "1"\n'
        template.append(instruction)
        template.append('headline:"%s"\nresponse:')
        return '\n'.join(template)

    def make_headlines_by_rating():
        headlines_by_rating = [[] for _ in range(11)]
        for headline, score in human_ratings:
            headlines_by_rating[score].append((headline, score))
        return headlines_by_rating

    while True:
        yield '''Examples:

    headline:"Keep it simple"
    response:1

    headline:"Keeping laptop from frying in hot car"
    response:1

    headline:"MEGATHREAD: U.S. House Ukraine Aid vote has passed!"
    response:2

    headline:"Anthony Broadwater spent 16 years in prison after being wrongly convicted of raping Alice Sebold in 1981. This is his reaction to being exonerated in 2021. In 2023, he was awarded a $5.5 million payment from the State of New York."
    response:2

    headline:"When your friend got lost in Russian fairy tales, but you quickly brought him back to reality"
    response:4

    headline:"Interview with Andrew Cauchi, the father of Joel Cauchi, who carried out the attack at the Westfield Shopping Centre in Australia on April 13, 2024. Joel fatally stabbed six people before being shot to death by a police officer."
    response:6

    headline:"Meet the ‘pursuer of nubile young females’ who helped pass Arizona’s 1864 abortion law"
    response:8

    headline:"Parents of emaciated Lacey Fletcher, who was found dead, fused to a sofa and caked in her own waste, face 40 years in prison after pleading 'no contest' to manslaughter"
    response:10

    headline:"Wyoming hunter, 42, poses with exhausted wolf he tortured and paraded around his local bar with its mouth taped shut before shooting it dead - as his family member reenacts the sick scene"
    response:10

    headline:"Footage from 2009 shows Ericka McElroy in police custody after being arrested following the death of her husband. She allegedly fired a shotgun into the chest of her 37-year-old husband, Shane McElroy, following a domestic dispute."
    response:8

    Fill in the next headline's rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don't have enough info, respond with "1"

    headline:"%s"
    response:'''

#         yield '''Examples:
# 
# headline:"Wonder what kind of bike he bought?"
# response:1
# 
# headline:"Is a sink worth it?"
# response:1
# 
# headline:"Any layouts like this?"
# response:1
# 
# headline:"Question about DC DC installation"
# response:1
# 
# headline:"Jennifer and James Crumbley, parents of Michigan school shooter, sentenced to 10 to 15 years for manslaughter"
# response:6
# 
# headline:"Sedona City Council (city in Arizona) voted to allow workers to sleep in their cars because there's no affordable housing"
# response:4
# 
# headline:"TIL that King James VI of Scotland and I of England (1566–1625) enjoyed the company of handsome young men, shared his bed with his favourites and was often passionate in his expressions of love for them. He railed fiercely against sodomy."
# response:6
# 
# headline:"Several nazi billboards started popping up in Michigan."
# response:4
# 
# headline:"Parents of emaciated Lacey Fletcher, who was found dead, fused to a sofa and caked in her own waste, face 40 years in prison after pleading 'no contest' to manslaughter"
# response:10
# 
# headline:"A Chicago woman accused of luring a pregnant teenager to her home and cutting her baby from her womb with a butcher knife nearly five years ago pleaded guilty to murder Tuesday and was sentenced to 50 years in prison."
# response:10
# 
# headline:"Sacramento sex offender pleads guilty to running child pornography websites"
# response:7
# 
# Fill in the next headline's rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don't have enough info, respond with "1"
# 
# headline:"%s"
# response:
# '''
        headlines_by_rating = make_headlines_by_rating()
        low_ratings = [r for rating_list in headlines_by_rating[:4] for r in rating_list]
        medium_ratings = [r for rating_list in headlines_by_rating[4:7] for r in rating_list]
        high_ratings = [r for rating_list in headlines_by_rating[7:] for r in rating_list]
        sampled_ratings = (
            random.sample(low_ratings, random.randint(1, 5)) +
            random.sample(medium_ratings, random.randint(1, 5)) +
            random.sample(high_ratings, random.randint(1, 5))
        )
        yield make_format_helper(sampled_ratings)


def get_llm_rating(prompt_format, headline, retry=0, model='llama3'):
    prompt = prompt_format % headline
    json_dict = {
        'model': model,
        'Stream': False,
        'prompt': prompt,
        'options': { "num_predict": 2 },
        # 'keep_alive': '10m',
    }
    res = requests.post('http://localhost:11434/api/generate', json=json_dict)
    llm_response = res.json()['response']
    # print(headline)
    # print(llm_response)
    try:
        llm_response = int(llm_response)
    except ValueError:
        if retry < 5:
            return get_llm_rating(prompt_format, headline, retry=retry+1, model=model)
        else:
            return 25, 5
    return llm_response, retry + 1

# Initialize accuracy metrics
def get_model_accuracy(model, prompt_format):
    correct = 0
    total = 0
    sq_error = 0
    high_rb_correct = 0
    high_rb_total = 0
    low_rb_correct = 0
    low_rb_total = 0
    retries = 0
    nonint = 0

    start = time.time()
    for headline, human_rating in human_ratings:
        if headline in prompt_format:
            continue

        # llm_rating, retry = get_llm_rating(prompt_format, headline, model=model)

        rating_l, retry_l = zip(*[
            get_llm_rating(prompt_format, headline, model=model)
            for _ in range(10)
        ])
        llm_rating, retry = sum(rating_l) / len(rating_l), sum(retry_l)

        int_rating = True
        try:
            llm_rating = int(llm_rating)
            error = human_rating - llm_rating
        except ValueError:
            int_rating = False
            error = 9  # max error
            nonint += 1

        if int_rating and abs(llm_rating - human_rating) <= 2.0:
            correct += 1

        if human_rating > 5:
            high_rb_total += 1
            if int_rating and llm_rating > 5:
                high_rb_correct += 1

        if human_rating < 4:
            low_rb_total += 1
            if int_rating and llm_rating < 4:
                low_rb_correct += 1

        total += 1
        sq_error += error ** 2
        retries += retry
    end = time.time()

    # Calculate overall accuracy
    avg_mse = sq_error / total
    accuracy = correct / total * 100
    high_accuracy = high_rb_correct / (high_rb_total or 1) * 100
    low_accuracy = low_rb_correct / (low_rb_total or 1) * 100
    hilo = (high_accuracy + low_accuracy) / 2
    avg_tries = retries / total
    avg_nonint = nonint / total * 100
    avg_ms = int((end - start) / total * 1000)
    return avg_mse, accuracy, high_accuracy, low_accuracy, hilo, avg_tries, avg_nonint, avg_ms


def main():
    for prompt_format in make_prompt_format():
        print('\n', prompt_format)
        for model in [
                'phi3',
                'llama3',
                # 'phi3:medium',
                # 'starling-lm',
                # 'openhermes',
                # 'dolphin-llama3',
                # 'llama2-uncensored',
                # 'gemma',
                # 'solar',
        ]:
            error, ac, high_ac, low_ac, hilo_ac, tries, nonint, avg_ms = get_model_accuracy(model, prompt_format)
            separator = ' ' * 5
            print(separator.join([
                f'{model:17s}',
                f'er {error:4.1f}',
                f'ac2 {ac:3.0f}%',
                f'hi {high_ac:3.0f}%',
                f'low {low_ac:3.0f}%',
                f'hilo {hilo_ac:3.0f}%',
                f'try {tries:4.2f}',
                f'nint {nonint:3.0f}%',
                f'{avg_ms:4d}ms'
            ]))

if __name__ == '__main__':
    main()

'''
 Rate whether this headline elicits anger on a scale 1-10. 1 means no anger.  10 means lots of anger. "%s" Reply with a single number.
starling-lm          er  3.7    ac2  88%    hi  71%    low  90%    hilo  80%    try 1.02    nint   0%     400ms
openhermes           er  7.7    ac2  69%    hi  86%    low  66%    hilo  76%    try 1.02    nint   0%     412ms
llama3               er 25.5    ac2  39%    hi  93%    low  36%    hilo  64%    try 1.82    nint  11%     515ms
dolphin-llama3       er 29.5    ac2  20%    hi  64%    low  13%    hilo  38%    try 2.20    nint  18%     555ms
llama2-uncensored    er 38.2    ac2  13%    hi  93%    low   7%    hilo  50%    try 1.84    nint  10%     529ms
gemma                er 54.0    ac2   5%    hi  71%    low   1%    hilo  36%    try 3.43    nint  37%     874ms
solar                er 80.6    ac2   0%    hi   0%    low   1%    hilo   0%    try 5.98    nint 100%    1547ms

 Examples:

headline:"California man sentenced to 40 years to life for fatal freeway shooting of 6-year-old boy during road rage incident"
response:9

headline:"Iran launched dozens of drones toward Israel - report"
response:1

headline:"A gang of Robber crabs invade a family picnic in Australia"
response:1


Fill in the next headline's rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don't have enough info, respond with "0"

headline:"%s"
response:
starling-lm          er  6.1    ac2  81%    hi  93%    low  80%    hilo  86%    try 1.00    nint   0%     425ms
openhermes           er  9.8    ac2  63%    hi  86%    low  60%    hilo  73%    try 1.00    nint   0%     413ms
llama3               er  8.3    ac2  73%    hi  86%    low  72%    hilo  79%    try 1.00    nint   0%     425ms
dolphin-llama3       er 26.1    ac2  15%    hi 100%    low   7%    hilo  53%    try 1.00    nint   0%     420ms
llama2-uncensored    er 26.7    ac2  36%    hi  50%    low  35%    hilo  43%    try 1.28    nint   4%     465ms
gemma                er  8.3    ac2  79%    hi  93%    low  83%    hilo  88%    try 1.01    nint   0%     484ms
solar                er  7.3    ac2  84%    hi  43%    low  92%    hilo  67%    try 1.39    nint   6%     688ms

 Rate how much this headline is taking pleasure at something bad happening to someone on a scale 1-9. Your reply should be 1 character long. Reply "1" if not sure.'

headline: "%s"
starling-lm          er  4.3    ac2  87%    hi  71%    low  90%    hilo  80%    try 1.00    nint   0%     408ms
openhermes           er 18.0    ac2  48%    hi  93%    low  45%    hilo  69%    try 1.01    nint   0%     405ms
llama3               er 21.8    ac2  52%    hi  71%    low  51%    hilo  61%    try 1.89    nint  13%     538ms
dolphin-llama3       er 15.9    ac2  62%    hi  36%    low  64%    hilo  50%    try 1.52    nint   4%     481ms
llama2-uncensored    er 21.1    ac2  49%    hi  43%    low  51%    hilo  47%    try 1.09    nint   0%     421ms
gemma                er  9.6    ac2  67%    hi  93%    low  64%    hilo  78%    try 1.10    nint   0%     485ms
solar                er 30.7    ac2  59%    hi  14%    low  65%    hilo  40%    try 3.13    nint  37%    1022ms

 On a scale 1-10, how ragebaity is this headline?  "%s".  Reply with a single number only.
starling-lm          er  6.9    ac2  78%    hi  86%    low  77%    hilo  81%    try 1.00    nint   0%     490ms
openhermes           er 21.5    ac2  34%    hi 100%    low  27%    hilo  64%    try 1.05    nint   0%     473ms
llama3               er 17.9    ac2  32%    hi 100%    low  25%    hilo  63%    try 1.00    nint   0%     453ms
dolphin-llama3       er 30.1    ac2  20%    hi  71%    low  13%    hilo  42%    try 2.41    nint  22%     656ms
llama2-uncensored    er 36.7    ac2  14%    hi  71%    low   8%    hilo  40%    try 1.81    nint  10%     593ms
gemma                er 39.5    ac2  14%    hi 100%    low   9%    hilo  55%    try 2.08    nint  17%     704ms
solar                er 63.0    ac2  22%    hi   0%    low  25%    hilo  12%    try 5.10    nint  78%    1545ms

 Rate whether this headline is trying to elicit specifically anger on a scale 1-10? "%s" Reply with a single number only.
starling-lm          er  3.1    ac2  90%    hi  29%    low  94%    hilo  62%    try 1.00    nint   0%     502ms
openhermes           er 11.8    ac2  58%    hi  93%    low  55%    hilo  74%    try 1.00    nint   0%     472ms
llama3               er 27.2    ac2  16%    hi 100%    low  10%    hilo  55%    try 1.00    nint   0%     468ms
dolphin-llama3       er 16.3    ac2  33%    hi 100%    low  25%    hilo  63%    try 1.54    nint   5%     523ms
llama2-uncensored    er 38.8    ac2   9%    hi 100%    low   3%    hilo  51%    try 1.22    nint   2%     491ms
gemma                er 44.1    ac2   8%    hi  86%    low   4%    hilo  45%    try 1.70    nint  10%     590ms
solar                er 80.7    ac2   0%    hi   7%    low   0%    hilo   4%    try 5.98    nint 100%    1524ms

Examples:

headline:"How the tree is peeled for cinamon"
response:1

headline:"Sedona City Council (city in Arizona) voted to allow workers to sleep in their cars because there's no affordable housing"
response:4

headline:"Idaho Lawmaker Asks If Swallowing Small Camera Could Allow Remote Gynecological Exams"
response:5

headline:"She Painted a Few Champagne Bottles. Then Came Meta’s Customer Support Hell"
response:4

headline:"Parents of emaciated Lacey Fletcher, who was found dead, fused to a sofa and caked in her own waste, face 40 years in prison after pleading 'no contest' to manslaughter"
response:10

headline:"Wyoming hunter, 42, poses with exhausted wolf he tortured and paraded around his local bar with its mouth taped shut before shooting it dead - as his family member reenacts the sick scene"
response:10

Fill in the next headline's rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don't have enough info, respond with "1"

headline:"%s"
response:
starling-lm           er  6.6     ac2  81%     hi 100%     low  79%     hilo  90%     try 1.00     nint   0%      335ms
openhermes            er  5.1     ac2  79%     hi  83%     low  76%     hilo  80%     try 1.00     nint   0%      338ms
llama3                er  3.4     ac2  88%     hi 100%     low  89%     hilo  95%     try 1.00     nint   0%      406ms
gemma                 er  8.7     ac2  77%     hi 100%     low  76%     hilo  88%     try 1.00     nint   0%      494ms
solar                 er 33.1     ac2  58%     hi   0%     low  60%     hilo  30%     try 3.35     nint  40%     1102ms

llama3                er  3.9     ac2  84%     hi  86%     low  83%     hilo  85%     try 1.00     nint   0%      334ms
llama3                er  8.7     ac2  73%     hi  86%     low  70%     hilo  78%     try 1.31     nint   4%      348ms
llama3                er  3.1     ac2  86%     hi  82%     low  88%     hilo  85%     try 1.00     nint   0%      314ms
llama3                er  6.6     ac2  78%     hi  92%     low  74%     hilo  83%     try 1.02     nint   0%      344ms
llama3                er  3.8     ac2  83%     hi  86%     low  83%     hilo  85%     try 1.00     nint   0%      395ms
llama3                er  2.9     ac2  89%     hi  71%     low  92%     hilo  81%     try 1.00     nint   0%      393ms
llama3                er  3.3     ac2  85%     hi  95%     low  84%     hilo  90%     try 1.00     nint   0%      412ms
llama3                er  3.8     ac2  84%     hi  91%     low  83%     hilo  87%     try 1.00     nint   0%      428ms
llama3                er  3.5     ac2  87%     hi  91%     low  86%     hilo  88%     try 1.00     nint   0%      432ms
llama3                er  3.4     ac2  88%     hi  81%     low  88%     hilo  85%     try 1.00     nint   0%      446ms
llama3                er  3.2     ac2  87%     hi  91%     low  89%     hilo  90%     try 1.00     nint   0%      456ms
llama3                er  4.3     ac2  84%     hi  91%     low  82%     hilo  87%     try 1.02     nint   0%      462ms
llama3                er  3.9     ac2  84%     hi  77%     low  83%     hilo  80%     try 1.00     nint   0%      474ms
llama3                er  3.1     ac2  90%     hi  59%     low  94%     hilo  77%     try 1.00     nint   0%      468ms
llama3                er  3.4     ac2  86%     hi  91%     low  87%     hilo  89%     try 1.00     nint   0%      497ms
llama3                er  4.7     ac2  83%     hi  96%     low  81%     hilo  88%     try 1.00     nint   0%      483ms
llama3                er  4.0     ac2  83%     hi  86%     low  85%     hilo  86%     try 1.00     nint   0%      505ms
llama3                er  3.8     ac2  85%     hi  83%     low  84%     hilo  83%     try 1.00     nint   0%      514ms
llama3                er  3.2     ac2  85%     hi  86%     low  83%     hilo  85%     try 1.00     nint   0%      534ms
llama3                er  3.2     ac2  87%     hi  82%     low  88%     hilo  85%     try 1.00     nint   0%      531ms


'''

'''Examples:

headline:"Wonder what kind of bike he bought?"
response:Headline refers to someone buying a bicycle.  Nothing rage-baity.
1

headline:"Is a sink worth it?"
response:Headline is contemplating about installing a sink. Not ragebait.
1

headline:"Any layouts like this?"
response:Headline asking for feedback on some kind of layout.  Not ragebait.
1

headline:"Question about DC DC installation"
response:Headline asking for feedback on electric setup.
1

headline:"Jennifer and James Crumbley, parents of Michigan school shooter, sentenced to 10 to 15 years for manslaughter"
response:Headline refers to parents of a school shooter going to jail.  This evokes feelings of righteousness at the punishment of wrong-doers.
6

headline:"Sedona City Council (city in Arizona) voted to allow workers to sleep in their cars because there's no affordable housing"
response:Headline is informative, but also conceals some outrage at people having to sleep in their cars due to a lack of housing.
4

headline:"TIL that King James VI of Scotland and I of England (1566–1625) enjoyed the company of handsome young men, shared his bed with his favourites and was often passionate in his expressions of love for them. He railed fiercely against sodomy."
response:Headline contains outrage at the hypocricy of a figure in power hurting gay people while being gay himself.
6

headline:"Several nazi billboards started popping up in Michigan."
response:Headline contains outrage at symbols of nazism appearing in public, in the US.
4

headline:"Parents of emaciated Lacey Fletcher, who was found dead, fused to a sofa and caked in her own waste, face 40 years in prison after pleading 'no contest' to manslaughter"
response:Headline describes an extreme case of neglect and abuse of a powerless child by the parents.  There are also feelings righeousness at their punishment, elevating the level of ragebait.
10

headline:"A Chicago woman accused of luring a pregnant teenager to her home and cutting her baby from her womb with a butcher knife nearly five years ago pleaded guilty to murder Tuesday and was sentenced to 50 years in prison."
response:Headline contains extreme violence directed at a teenager and her unborn child, and righteousness at the wrongdoer being pushished.  Extreme ragebait.
10

headline:"Sacramento sex offender pleads guilty to running child pornography websites"
response:Headline describes a child pornographer being punished.  Righteous ragebait.
7


Give your reasoning for whether the following headline contains ragebait.
The last line of your response should contain ONLY a single number 1-10 representing the ragebait score, with no label.
If the headline is not regabait, give it a score of 1.
A score of 5 is medium rage-baity.
If the headline is extremely rage-baity, give it a high score 8-10.

headline:"%s"
response:
'''
'''
 Examples:

    headline:"Keep it simple"
    response:1

    headline:"Keeping laptop from frying in hot car"
    response:1

    headline:"MEGATHREAD: U.S. House Ukraine Aid vote has passed!"
    response:2

    headline:"Anthony Broadwater spent 16 years in prison after being wrongly convicted of raping Alice Sebold in 1981. This is his reaction to being exonerated in 2021. In 2023, he was awarded a $5.5 million payment from the State of New York."
    response:2

    headline:"When your friend got lost in Russian fairy tales, but you quickly brought him back to reality"
    response:4

    headline:"Interview with Andrew Cauchi, the father of Joel Cauchi, who carried out the attack at the Westfield Shopping Centre in Australia on April 13, 2024. Joel fatally stabbed six people before being shot to death by a police officer."
    response:6

    headline:"Meet the ‘pursuer of nubile young females’ who helped pass Arizona’s 1864 abortion law"
    response:8

    headline:"Parents of emaciated Lacey Fletcher, who was found dead, fused to a sofa and caked in her own waste, face 40 years in prison after pleading 'no contest' to manslaughter"
    response:10

    headline:"Wyoming hunter, 42, poses with exhausted wolf he tortured and paraded around his local bar with its mouth taped shut before shooting it dead - as his family member reenacts the sick scene"
    response:10

    headline:"Footage from 2009 shows Ericka McElroy in police custody after being arrested following the death of her husband. She allegedly fired a shotgun into the chest of her 37-year-old husband, Shane McElroy, following a domestic dispute."
    response:8

    Fill in the next headline's rage-bait score with a value 1-10.  Respond with ONLY a single number. If you don't have enough info, respond with "1"

    headline:"%s"
    response:
llama3                er  2.0     ac2  90%     hi  73%     low  97%     hilo  85%     try 10.01     nint   0%     1561ms
phi3:medium           er  2.4     ac2  91%     hi  55%     low  95%     hilo  75%     try 10.00     nint   0%     3188ms
phi3                  er 11.1     ac2  58%     hi 100%     low  55%     hilo  77%     try 10.00     nint   0%     1140ms
'''
