// ==UserScript==
// @name        Filter Subreddits
// @namespace   sergei@khan
// @include     *//*.reddit.com/*
// @version     1
// @icon        https://reddit.com/favicon.ico
// @grant       none
// ==/UserScript==

hideRagebait = true
ragebaitCutoff = 7

const domainBanlist = new Set([
  // tabloids
  'thedailybeast.com',
  'dailymail.co.uk',
]);

const titleBanlist = new Set([
  'giveaway',
  're giving away',
  // Pick x to be on your team, and the rest try to kill you spam
  'rest try to kill',
  '. go!',
  'boebert',
  'trump',
  'ocasio',
  // what movie has the best villain?
  'what movie',
  'what game',
  'cybertruck',
]);

const subredditBanlist = new Set([
  // Violence / hate / outrage / righteousness
  'r/abruptchaos',
  'r/actualpublicfreakouts',
  'r/antiwork',
  'r/assholedesign',
  'r/awfuleverything',
  'r/agedlikemilk',
  'r/bad_cop_no_donut',
  'r/badroommates',
  'r/boomersbeingfools',
  'r/byebyejob',
  'r/choosingbeggars',
  'r/combatfootage',
  'r/crappydesign',
  'r/crazyfuckingvideos',
  'r/cringe',
  'r/cringepics',
  'r/cringetopia',
  'r/cringevideo',
  'r/diwhy',
  'r/gatekeeping',
  'r/holdmycosmo',
  'r/holdmyfeedingtube',
  'r/iamatotalpieceofshit',
  'r/facepalm',
  'r/fluentinfinance',
  'r/fragilewhiteredditor',
  'r/fuckyoukaren',
  'r/hermancainaward',
  'r/idiotsincars',
  'r/imthemaincharacter',
  'r/insaneparents',
  'r/insanepeoplefacebook',
  'r/instagramreality',
  'r/instant_regret',
  'r/instantkarma',
  'r/justiceserved',
  'r/justneckbeardthings',
  'r/kidsarefuckingstupid',
  'r/livestreamfail',
  'r/leopardsatemyface',
  'r/maliciouscompliance',
  'r/mildlybaddrivers',
  'r/murderedbyaoc',
  'r/murderedbywords',
  'r/makemesuffer',
  'r/nahopwasrightfuckthis',
  'r/newsofthestupid',
  'r/niceguys',
  'r/noahgettheboat',
  'r/notliketheothergirls',
  'r/ohnoconsequences',
  'r/pettyrevenge',
  'r/politics',
  'r/publicfreakout',
  'r/quityourbullshit',
  'r/rareinsults',
  'r/roastme',
  'r/sadcringe',
  'r/sadposting',
  'r/selfawarewolves',
  'r/stupidfood',
  'r/texts',
  'r/thatsinsane',
  'r/therewasanattempt',
  'r/toiletpaperusa',
  'r/trashy',
  'r/twohottakes',
  'r/watchpeopledieinside',
  'r/whatcouldgowrong',
  'r/winstupidprizes',

  // Bull
  'r/amioverreacting',
  'r/amitheasshole',
  'r/amiwrong',
  'r/aitah',
  'r/aita_wibta_public',
  'r/amiugly',
  'r/tifu',
  'r/trueoffmychest',
  'r/unpopularopinion',

  // Not interesting
  'r/ask',
  'r/askmen',
  'r/askouija',
  'r/askreddit',
  'r/atheism',
  'r/blessedcomments',
  'r/blessedimages',
  'r/blursedcomments',
  'r/blursedimages',
  'r/boneappletea',
  'r/bonehurtingjuice',
  'r/boomershumor',
  'r/cats',
  'r/clevercomebacks',
  'r/comedyheaven',
  'r/comedyhell',
  'r/comedynecromancy',
  'r/comics',
  'r/cursedcomments',
  'r/cursedimages',
  'r/entertainment',
  'r/explainthejoke',
  'r/gaming',
  'r/gamingcirclejerk',
  'r/genz',
  'r/getmotivated',
  'r/holup',
  'r/imsorryjon',
  'r/jokes',
  'r/legaladvice',
  'r/mildlyinfuriating',
  'r/mildlyinteresting',
  'r/money',
  'r/movies',
  'r/moviedetails',
  'r/namemycat',
  'r/nostupidquestions',
  'r/notinteresting',
  'r/peterexplainsthejoke',
  'r/povertyfinance',
  'r/relationship_advice',
  'r/shitpostcrusaders',
  'r/starterpacks',

  // Don't care
  'r/android',
  'r/amcstock',
  'r/apple',
  'r/askuk',
  'r/baseball',
  'r/bbq',
  'r/bokunoheroacademia',
  'r/canada',
  'r/callofduty',
  'r/casualuk',
  'r/cfb',
  'r/cfl',
  'r/collegebasketball',
  'r/cricket',
  'r/destinythegame',
  'r/doctorwho',
  'r/eldenring',
  'r/fantasyfootball',
  'r/fauxmoi',
  'r/formula1',
  'r/globaloffensive',
  'r/genshin_impact_leaks',
  'r/genshin_impact',
  'r/gme',
  'r/halo',
  'r/hololive',
  'r/honkaistarrail',
  'r/honkaistarrail_leaks',
  'r/hockey',
  'r/jordanpeterson',
  'r/leagueoflegends',
  'r/marvelstudios',
  'r/millennials',
  'r/minecraft',
  'r/mma',
  'r/nba',
  'r/nfl',
  'r/onepiece',
  'r/pewdiepiesubmissions',
  'r/pokemon',
  'r/politicalhumor',
  'r/popculturechat',
  'r/prequelmemes',
  'r/ps4',
  'r/ps5',
  'r/playstation',
  'r/royalsgossip',
  'r/soccer',
  'r/squaredcircle',
  'r/starwars',
  'r/strangerthings',
  'r/sipstea',
  'r/superstonk',
  'r/superman',
  'r/taylorswift',
  'r/teenagers',
  'r/tennis',
  'r/toolband',
  'r/ufos',
  'r/wallstreetbets',
  'r/wutheringwaves',
  'r/wwe',
  'r/xboxone',

  // spam
  'r/mechanicalkeyboards',
  'r/videogames',
])


function filterDomains(){
  let domains = document.querySelectorAll('.link .domain')
  let hid = 0
  for (let sr of domains) {
    const domainNoparens = sr.textContent.toLowerCase().substr(1).slice(0, -1);
    if (domainBanlist.has(domainNoparens)) {
      let story = getStoryElement(sr)
      if (story) {
        hid += 1
        console.log('HIDING domain',
          domainNoparens,
          story.getElementsByClassName('title')[0].textContent
        )
        story.remove()
      }
    }
  }
  console.log(`\nHid ${hid} stories for domain`)
}

function filterTitles(){
  let titles = document.querySelectorAll('.link .title .may-blank')
  let hid = 0
  for (let title of titles) {
    for (let bannedTitle of titleBanlist) {
      if (title.text.toLowerCase().includes(bannedTitle)) {
        let story = getStoryElement(title)
        if (story) {
          hid += 1
          console.log('HIDING title:',
            bannedTitle,
            story.getElementsByClassName('title')[0].textContent
          )
          story.remove()
        }
      }
    }
  }
  console.log(`\nHid ${hid} stories for title`)
}

function filterSubreddits(){
  let subreddits = document.querySelectorAll('.link .subreddit')
  let hid = 0
  for (let sr of subreddits) {
    if (subredditBanlist.has(sr.text.toLowerCase())) {
      let story = getStoryElement(sr)
      if (story) {
        hid += 1
        console.log('HIDING subreddit',
          sr.text,
          story.getElementsByClassName('title')[0].textContent
        )
        story.remove()
      }
    }
  }
  console.log(`\nHid ${hid} stories for subreddit`)
}

function getStoryElement(child) {
  while (child) {
    if (child.classList && child.classList.contains('link')) return child
    child = child.parentElement
  }
}

function removeUnwantedElements() {
  let selectors = ['.listingsignupbar', '#searchexpando', '#search',
    '.premium-banner-outer', '#login_login-main', '.submit-link',
    '.submit-text', '.trending-subreddits', '.footer-parent',
    '.happening-now', '.infobar-toaster-container',
    '.login-required', '#sr-header-area', '.share',
    '.rank', '#header-bottom-right', '.flairrichtext', '.thumbnail',
    '.linkflairlabel', '.link.promoted', 'div:has(> .promoted-tag)']
  for (let selector of selectors) {
    for (let el of document.querySelectorAll(selector)) {
      el.remove()
    }
  }
  for (let selector of ['.hide-button']) {
    for (let el of document.querySelectorAll(selector)) {
      el.parentNode.remove()
    }
  }
}


///////////////////////////////////////////////////////////////////////////////

const subredditRegex = /reddit\.com\/r\/[^/]+/;
const commentsRegex = /reddit\.com\/r\/[^/]+\/comments/;

function isOnSubredditView() {
  return subredditRegex.test(window.location.href) &&
        !commentsRegex.test(window.location.href);
}

function isOnCommentView() {
  return commentsRegex.test(window.location.href);
}

function editCommentsView() {
  if (!isOnCommentView()) return;
  console.log('editing comments view')

  const selectors = [
    '.flat-list', // permalink/embed/parent links under each comment
    '.infobar', // textbox to leave comment
  ]
  for (let selector of selectors) {
    for (let el of document.querySelectorAll(selector)) {
      el.remove()
    }
  }
}


///////////////////////////////////////////////////////////////////////////////

function editSubredditView() {
  // Move timestamp only on subreddit view, not comment threads
  if (isOnCommentView()) return;
  console.log('editing subreddit view')

  for (let link of document.querySelectorAll('.link')) {
    try {
      const selectors = ['.subreddit', '.live-timestamp']
      for (let selector of selectors) {
        let target = link.querySelectorAll(selector)[0]
        if (!target) continue
        let commentList = link.querySelectorAll('.flat-list')[0]
        const li = document.createElement("li");
        li.appendChild(target)
        commentList.appendChild(li)
      }
      for (let el of link.querySelectorAll('.tagline')) {
        el.remove()
      }
    } catch (e) {
      console.log('error moving subreddit:', e)
    }
  }
}


///////////////////////////////////////////////////////////////////////////////

function addStyles() {
  var styles = `
    .buttons > li > a, .selected, .choice{
      font-weight: normal !important;
    }
    .next-button a, .prev-button a {
      font-weight: normal !important;
      background: inherit !important;
      border: 0 !important;
    }
    .buttons > li {
      padding-right: 0 !important;
    }
    .link .score {
      font-family: helvetica !important;
      font-weight: lighter !important;
      font-size: 12px !important;
      padding-top: 6px !important;
    }
    .expando-button {
      font-family: helvetica !important;
      font-weight: lighter !important;
      font-size: 14px !important;
      height: 14px !important;
      width: 14px !important;
      background-image: none !important;
    }
    .expando-button:hover {
      filter: invert(.5) !important;
    }
    .expando-button.collapsed:before {
      content: "+";
    }
    .expando-button.expanded:before {
      content: "-";
    }
    .comment .author {
      font-weight: normal !important;
    }
    a.author.submitter {
      color: red;
    }
    `
  var styleSheet = document.createElement("style")
  styleSheet.innerText = styles
  document.head.appendChild(styleSheet)

  // Disable custom subreddit css
  try {
    document.querySelectorAll('link[title="applied_subreddit_stylesheet"]')[0].remove()
  } catch (e) {}
}


///////////////////////////////////////////////////////////////////////////////

async function addRageScores(){
  let titles = document.querySelectorAll('a.title')
  for (let title of titles) {
    replaceTitle(title)
  }
}

async function replaceTitle(title, retry = 0) {
  // Fill in rage-bait score (1-10).  Respond with a single number and nothing else.  If you don't have enough info, respond with "1"
  let prompt = `Examples:

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

    headline:"${title.text}"
    response:`

  let score
  try {
    askLLM(prompt, retry).then(score => {
      score = score.trim()
      // console.log('ragebait score', title.text, score)
      if (!isNumeric(score) && retry < 10) {
        console.log('retrying', title.text, score)
        replaceTitle(title, retry + 1)
      } else {
        title.text = `${Math.round(score)}|${title.text}`
        if (score > ragebaitCutoff) {
            title.style.filter = 'opacity(.5)'
            if (hideRagebait) {
                let story = getStoryElement(title)
                story.remove()
                console.log('HIDING ragebait:', title.text)
            }
        }
      }
    })
  } catch (e) {}
}

function isNumeric(str) {
  if (typeof str != "string") return false // we only process strings!  
  return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
         !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

async function askLLM(prompt, retry) {
 // const response = await fetch('http://localhost:11434/api/generate', {
  const response = await fetch('http://localhost:5000/cached-llm', {
    method: 'POST',
    headers: {'Content-Type': 'application/json; charset=UTF-8text/json' },
    body: JSON.stringify({
      model: "llama3",
      Stream: false,
      prompt: prompt,
      bust_cache: retry > 0,
      options: {
        // Ask for 2 tokens only
        "num_predict": 2
      }
    })
  });

  const r = await response.json();
  return r.response
}


///////////////////////////////////////////////////////////////////////////////

function addExpandButton() {
  console.log('adding expand button')
  const tabs = document.querySelector('.tabmenu')
  const li = document.createElement("li");
  const a = document.createElement("a");
  a.innerText = 'expand all'
  a.classList.add('choice')
  a.href = 'javascript:void(0)'
  li.appendChild(a)
  tabs.appendChild(li)
  li.onclick = function() {
      document.querySelectorAll('.expando-button').forEach(e => e.click())
      setTimeout(() =>
          document.querySelectorAll('button[data-action=pause]').forEach(p => p.click()),
          100)
  }
}


///////////////////////////////////////////////////////////////////////////////

function addHideButton() {
  console.log('adding hide button')
  const tabs = document.querySelector('.tabmenu')
  const li = document.createElement("li");
  const a = document.createElement("a");
  a.innerText = 'hide all'
  a.classList.add('choice')
  a.href = 'javascript:void(0)'
  li.appendChild(a)
  tabs.appendChild(li)
  li.onclick = function() {
    const urls = Array.from(document.querySelectorAll('a.title'))
      .map(a => a.href)

    fetch('http://localhost:5000/url/hide', {
      method: 'POST',
      headers: {'Content-Type': 'application/json; charset=UTF-8text/json' },
      body: JSON.stringify({ urls }),
    }).then(() => {
      Array.from(document.querySelectorAll('a.title'))
        .map(title => getStoryElement(title).remove())
    })
  }
}

async function hideHiddenStories() {
  let titles = document.querySelectorAll('a.title')
  for (let title of titles) {
    askIfHidden(title.href, title.text).then(hidden => {
      if (hidden) {
        let story = getStoryElement(title)
        if (story) {
          console.log('HIDING marked hidden:', title.text)
          story.remove()
        }
      }
    })
  }
}

async function askIfHidden(url, title) {
 // const response = await fetch('http://localhost:11434/api/generate', {
  const response = await fetch('http://localhost:5000/url/is-hidden', {
    method: 'POST',
    headers: {'Content-Type': 'application/json; charset=UTF-8text/json' },
    body: JSON.stringify({ url, title })
  });

  const r = await response.json();
  return r.is_hidden
}


///////////////////////////////////////////////////////////////////////////////

const sleepMs = 10;
setTimeout(filterSubreddits, sleepMs);
setTimeout(filterDomains, sleepMs);
setTimeout(filterTitles, sleepMs);
setTimeout(addRageScores, sleepMs + 500);
setTimeout(removeUnwantedElements, sleepMs);
setTimeout(editSubredditView, sleepMs);
setTimeout(editCommentsView, sleepMs);
setTimeout(addStyles, sleepMs);
setTimeout(addHideButton, sleepMs);
setTimeout(addExpandButton, sleepMs + 50);
setTimeout(hideHiddenStories, sleepMs);
