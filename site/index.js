const m = require('mithril')
const stream = require('mithril/stream')
const { Kanjiapi } = require('kanjiapi-wrapper')
const { DateTime } = require('luxon')
const { LogProvider } = require('./log_provider');

const kanjiapi = Kanjiapi.build()
kanjiapi.addListener('app', m.redraw)

const KYOIKU_URL = 'https://en.wikipedia.org/wiki/Ky%C5%8Diku_kanji'
const JOYO_URL = 'https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji'
const JINMEIIYO_URL = 'https://en.wikipedia.org/wiki/Jinmeiy%C5%8D_kanji'
const GITHUB_URL = 'https://github.com/onlyskin/kanjiapi.dev'
const README_URL = 'https://github.com/onlyskin/kanjiapi.dev#readme'
const KANJI_URL = 'https://en.wikipedia.org/wiki/Kanji'
const MITHRIL_URL = 'https://mithril.js.org/'
const JLPT_URL = 'https://en.wikipedia.org/wiki/Japanese-Language_Proficiency_Test#Previous_format_(1984%E2%80%932009)'
const UNICODE_URL = 'https://en.wikipedia.org/wiki/Unicode'
const HEISIG_URL = 'https://en.wikipedia.org/wiki/Remembering_the_Kanji_and_Remembering_the_Hanzi'
const KANJIAPI_WRAPPER_URL = 'https://github.com/onlyskin/kanjiapi-wrapper'
const KANJIKAI_URL = 'https://kai.kanjiapi.dev'
const ONKUN_URL = 'https://www.onkun.org/'
const KANJIDOJO_URL = 'https://kanji-dojo.vercel.app/'
const EDRDG_URL = 'https://www.edrdg.org/'
const EDRDG_LICENCE_URL = 'https://www.edrdg.org/edrdg/licence.html'
const KANJIAPI_V1_URL = 'https://kanjiapi.dev/v1/'
const KANJI_FLASH_URL = 'https://www.kanjiflash.com'

const PopularityLogs = {
    log_display_count: 10,
    increment_log_display_count: function() {
        this.log_display_count = this.log_display_count * 2
    },
    longest_log_count: function() {
        return Math.max(
            this.topJoyo.length,
            this.topJinmeiyo.length,
            this.topHeisig.length,
            this.topOther.length,
        )
    },
    topAll: [],
    getTops: function() {
        if (
            kanjiapi.getJoyoSet().value &&
            kanjiapi.getJinmeiyoSet().value &&
            kanjiapi.getHeisigSet().value &&
            this.topJoyo.length === 0 &&
            !this.hasLoading()
        ) {
            this.getCollatedItems().forEach(item => {
                this.topAll.push(item);
                if (kanjiapi.getJoyoSet().value.has(item[0])) {
                    this.topJoyo.push(item);
                } else if (kanjiapi.getJinmeiyoSet().value.has(item[0])) {
                    this.topJinmeiyo.push(item);
                } else if (kanjiapi.getHeisigSet().value.has(item[0])) {
                    this.topHeisig.push(item);
                } else if (item[0].length === 1) {
                    this.topOther.push(item);
                } else {
                    this.topExtra.push(item);
                }
            });
            m.redraw();
        }
    },
    topJoyo: [],
    getTopJoyo: function() {
        this.getTops()
        return this.topJoyo;
    },
    topJinmeiyo: [],
    getTopJinmeiyo: function() {
        this.getTops()
        return this.topJinmeiyo;
    },
    topHeisig: [],
    getTopHeisig: function() {
        this.getTops()
        return this.topHeisig;
    },
    topOther: [],
    getTopOther: function() {
        this.getTops()
        return this.topOther;
    },
    topExtra: [],
    getTopExtra: function() {
        this.getTops()
        return this.topExtra;
    },
    getFlatSevenDaysHours: function() {
        const today = DateTime.utc().startOf('day')
        return [...Array(7).keys()]
            .map(i => today.minus({days: 7-i}))
            .map(d => [...Array(24).keys()].map(i => d.plus({hours: i})))
            .flat()
    },
    hasLoading: function() {
        const loadingRequests = this.getFlatSevenDaysHours()
            .map(d => log_provider.getLog(d.toISO()))
            .filter(res => res.status === 'LOADING');
        return loadingRequests.length > 0;
    },
    getCollatedItems: function() {
        return collateLogRequests(this.getFlatSevenDaysHours())
    },
}
const log_provider = new LogProvider()
log_provider.addListener('app', m.redraw)

const Link = {
    view: ({ children, attrs: { href } }) => m(
        'a.vermillion',
        { role: 'button', href },
        children
    ),
}

const InternalLink = {
    view: ({ children, attrs: { href } }) => m(
        m.route.Link,
        { role: 'button', href, class: 'vermillion' },
        children
    ),
}

const GithubIcon = {
    view: () => m(
        'svg',
        {
            'role': 'img',
            'width': '24',
            'height': '24',
            'viewBox': '0 0 24 24',
            'xmlns': 'http://www.w3.org/2000/svg'
        },
        [
            m('title', 'GitHub icon'),
            m('path', {
                'd': 'M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12'
            }),
        ],
    ),
}

const Footer = {
    view: () => m(
        '',
        { style: { 'height': '50px' } },
        m(Link, { href: GITHUB_URL }, m(GithubIcon)),
    ),
}

const Header = {
    view: () => m(
        '.border-box.pa2.pa3-l.white.w-100.bg-dark-ink',
        m('.tc.ma1.f2.f1-l.rounded', '漢字'),
        m('.tc.ma1.f2.f1-l', 'kanjiapi.dev'),
    )
}

const About = {
    view: () => [
        m('.f4.f3-l.tc.mv2.nowrap', 'What is this?'),
        m(
            '.self-start.pv2',
            'This is an API that provides JSON endpoints for over 13,000 ',
            m(Link, { href: KANJI_URL }, 'kanji'),
            ' using data from an extensive kanji dictionary.'
        ),
        m(
            '.self-start.pv2',
            'This API uses the EDICT and KANJIDIC dictionary files. ',
            'These files are the property of the ',
            m(
                Link,
                { href: EDRDG_URL },
                'Electronic Dictionary Research and Development Group',
            ),
            ', and are used in conformance with the Group\'s ',
            m(Link, { href: EDRDG_LICENCE_URL }, 'licence'),
            '.',
        ),
        m(
            '.self-start.pv2',
            'This page is built using ',
            m(Link, { href: MITHRIL_URL }, 'mithril.js'),
            '.',
        ),
        m('.f4.f3-l.tc.mv2.nowrap', 'Projects that use kanjiapi.dev'),
        m(
            '.self-start.pv2',
            m(Link, { href: KANJIKAI_URL }, 'kanjikai'),
            ': a rabbit hole kanji dictionary in which every character and every reading is clickable'
        ),
        m(
            '.self-start.pv2',
            m(Link, { href: ONKUN_URL }, 'onkun'),
            ': the simple kanji dictionary'
        ),
        m(
            '.self-start.pv2',
            m(Link, { href: KANJIDOJO_URL}, 'kanji dojo'),
            ': a place to learn new kanji vocabulary'
        ),
        m(
            '.self-start.pv2',
            m(Link, { href: KANJI_FLASH_URL}, 'kanji flash'),
            ': kanji flashcards by JLPT level and more'
        ),
        m(
            '.self-start.pv2',
            'Raise a ',
            m(Link, { href: GITHUB_URL }, 'PR'),
            ' to add your project here!'
        )
    ],
}

const Separator = {
    view: () => m('hr.w-100.black-50.mv4'),
}

const PopularityKanji = {
    view: ({ attrs: { kanji }}) => m(
        'a.black.no-underline.pointer',
        { href: `https://kai.kanjiapi.dev/#!/${kanji}` },
        kanji,
    ),
}

const KanjiPopularityColumn = {
    view: ({ attrs: { title, data } }) => m(
        '.h-100.w-25.flex.flex-column.justify-between.ph2.pv2.pv0-l',
        [
            m('.flex.items-start.justify-center.pb2', title),
            m(
                '',
                data.slice(0, PopularityLogs.log_display_count)
                   .map((item, index) => m('.flex.justify-center', [
                       m(
                           `.mr3`,
                           m(
                               PopularityKanji,
                               { kanji: `${item[0].length === 1 ? '' : '/'}${item[0]}` })
                       ),
                       m('', item[1]),
                   ])),
            ),
        ],
    ),
};

const ShowMoreLogsButton = {
    view: () => PopularityLogs.getTopJoyo().length !== 0 &&
        PopularityLogs.longest_log_count() > PopularityLogs.log_display_count ?  m(
            '.self-center.flex.flex-column.items-center.vermillion.pointer',
            { role: 'button', onclick: e => PopularityLogs.increment_log_display_count() },
            m('', '↓'),
            m('', 'show more'),
        ) : null,
}

const KanjiPopularity = {
    view: () => PopularityLogs.hasLoading() ? null : [
        m(
            '.flex.pt3',
            m(KanjiPopularityColumn, {title: 'Joyo only', data: PopularityLogs.getTopJoyo()}),
            m(KanjiPopularityColumn, {title: 'Jinmeiyō only', data: PopularityLogs.getTopJinmeiyo()}),
            m(KanjiPopularityColumn, {title: 'non-Jōyō, non-Jinmeiyō, in Heisig', data: PopularityLogs.getTopHeisig()}),
            m(KanjiPopularityColumn, {title: 'non-Jōyō, non-Jinmeiyō, non-Heisig kanji', data: PopularityLogs.getTopOther()}),
        ),
        m(ShowMoreLogsButton),
    ],
}

const Search = {
    view: ({ attrs: { path } }) => m(
        '.w-100.flex.items-stretch.mt1.mb0',
        m('label#search-label', KANJIAPI_V1_URL),
        m(
            'input[type=text]#search-input',
            {
                value: path(),
                onchange: e => path(e.target.value),
            },
        ),
    ),
}

const Example = {
    view: ({ attrs: { path, url } }) => m(
        '.di.i.underline.nowrap.vermillion.pointer',
        { role: 'button',  onclick: () => path(url) },
        url,
    ),
}

const Examples = {
    view: ({ attrs: { path } }) => m(
        '.f7.f6-l.self-start.mt0.mb1',
        'Hint: try ',
        m(Example, { path, url: 'kanji/蜜' }),
        ', ',
        m(Example, { path, url: 'kanji/grade-1' }),
        ', ',
        m(Example, { path, url: 'reading/あり' }),
        ', or ',
        m(Example, { path, url: 'words/蠍' }),
    ),
}

const SearchResult = {
    view: ({ attrs: { result } }) => m(
        '',
        {
            class: [ 'self-stretch', 'f7', 'f6-l', 'pa1', 'pa2-l', 'mv1',
                'ba', 'b--black-10', 'border-box', 'shadow-4', 'code', 'pre',
                'pre-wrap' ].join(' '),
        },
        result.status === Kanjiapi.SUCCESS ?
            JSON.stringify(result.value, null, 2) :
            result.status === Kanjiapi.LOADING ? 'Loading' :
            result.status === Kanjiapi.ERROR ? 'Not Found' : 'Error',
    ),
}

const JINMEIYO_LINK = {
    view: () => m(Link, { href: JINMEIIYO_URL }, 'Jinmeiyō kanji'),
}

const JOYO_LINK = {
    view: () => m(Link, { href: JOYO_URL }, 'Jōyō kanji'),
}

const HEISIG_LINK = {
    view: () => m(Link, { href: HEISIG_URL }, 'Heisig'),
}

const KYOIKU_LINK = {
    view: () => m(Link, { href: KYOIKU_URL }, 'Kyōiku kanji'),
}

const KANJI_LIST_ENDPOINTS = [
    { endpoint: '/v1/kanji/joyo', description: ['List of ', m(JOYO_LINK)]},
    { endpoint: '/v1/kanji/jouyou', description: ['List of ', m(JOYO_LINK)]},
    { endpoint: '/v1/kanji/jinmeiyo', description: ['List of ', m(JINMEIYO_LINK)]},
    { endpoint: '/v1/kanji/jinmeiyou', description: ['List of ', m(JINMEIYO_LINK)]},
    { endpoint: '/v1/kanji/heisig', description: ['List of kanji which have a ', m(HEISIG_LINK), ' keyword']},
    { endpoint: '/v1/kanji/kyouiku', description: ['List of all ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/kyoiku', description: ['List of all ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-1', description: ['List of Grade 1 ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-2', description: ['List of Grade 2 ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-3', description: ['List of Grade 3 ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-4', description: ['List of Grade 4 ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-5', description: ['List of Grade 5 ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-6', description: ['List of Grade 6 ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/grade-8', description: ['List of ', m(JOYO_LINK), ' excluding ', m(KYOIKU_LINK)]},
    { endpoint: '/v1/kanji/all', description: 'List of all 13,000+ available kanji' },
]

const KANJI_FIELDS = [
    { name: 'kanji', description: 'The kanji itself', type: 'string' },
    {
        name: 'kun_readings',
        description: 'A list of kun readings associated with the kanji',
        type: 'string[]'
    },
    {
        name: 'on_readings',
        description: 'A list of on readings associated with the kanji',
        type: 'string[]'
    },
    {
        name: 'name_readings',
        description: 'A list of readings that are only used in names associated with the kanji',
        type: 'string[]'
    },
    {
        name: 'meanings',
        description: 'A list of English meanings associated with the kanji',
        type: 'string[]'
    },
    {
        name: 'stroke_count',
        description: 'The number of strokes necessary to write the kanji',
        type: 'number'
    },
    {
        name: 'unicode',
        description: [
            'The ',
            m(Link, { href: UNICODE_URL }, 'Unicode'),
            ' codepoint of the kanji',
        ],
        type: 'string',
    },
    {
        name: 'grade',
        description: [
            'The official grade of the kanji (1-6 for ',
            m(KYOIKU_LINK),
            ', 8 for the remaining ',
            m(JOYO_LINK),
            ', 9 for ',
            m(JINMEIYO_LINK),
            ')',
        ],
        type: [ m('.di.f7', '1..6 | 8 | 9 | '), 'null' ],
    },
    {
        name: 'jlpt',
        description: [
            'The ',
            m(Link, { href: JLPT_URL }, 'former JLPT'),
            ' test level for the kanji',
        ],
        type: [ m('.di.f7', '1..4 | '), 'null'],
    },
    {
        name: 'heisig_en',
        description: [
          'The ',
          m(Link, { href: HEISIG_URL }, 'Heisig'),
          ' keyword associated with the kanji for English',
        ],
        type: [ 'string ', m('.di.f7', '|'), ' null' ],
    },
    {
        name: 'unihan_cjk_compatibility_variant',
        description: 'If the kanji is a compatibility variant character, the unified version of the character (see README.md Jinmeiyo section for more information)',
        type: [ 'string ', m('.di.f7', '|'), ' undefined' ],
    },
    {
        name: 'notes',
        description: 'Any notes about the kanji or its fields',
        type: 'string[]',
    },
]

const READING_FIELDS = [
    {
        name: 'reading',
        description: 'The reading itself',
        type: 'string'
    },
    {
        name: 'main_kanji',
        description: 'A list of kanji that use the associated reading',
        type: 'string[]'
    },
    {
        name: 'name_kanji',
        description: 'A list of kanji that use the associated reading exclusively in names',
        type: 'string[]'
    },
]

const WORD_FIELDS = [
    {
        name: 'meanings',
        description: 'A list of distinct meanings that the entry has',
        type: 'meaning[]'
    },
    {
        name: 'variants',
        description: 'A list of written variations for the entry',
        type: 'variant[]'
    },
]

const MEANING_FIELDS = [
    {
        name: 'glosses',
        description: 'A list of English equivalent terms for the particular meaning',
        type: 'string[]'
    },
]

const VARIANT_FIELDS = [
    {
        name: 'written',
        description: 'The written form of the variant',
        type: 'string'
    },
    {
        name: 'pronounced',
        description: 'The pronounced form of the variant (in kana)',
        type: 'string'
    },
    {
        name: 'priorities',
        description: 'A list of strings designating frequency lists in which the variant appears',
        type: 'string[]'
    },
]

const KanjiListEndpoint = {
    view: ({ attrs: { isLast, endpoint } }) => m(
        `.cf.pv2.pv0-l${isLast ? '.bn' : '.bb'}.b--silver`,
        m('.fl.w-100.w-third-l.pa1.code', `${endpoint.endpoint}`),
        m('.f7.f6-l.fl.w-100.w-two-thirds-l.pa1.i', endpoint.description),
    ),
}

const SchemaRow = {
    view: ({ attrs: { field, isLast } }) => m(
        `.cf.pv2.pv0-l${isLast ? '.bn' : '.bb'}.b--silver`,
        m('.f6.fl.w-50.w-third-l.pa1.code.truncate', `"${field.name}":`),
        m('.fl.w-50.w-third-l.pa1.code.small-caps.tr.tl-l', field.type),
        m('.f7.f6-l.fl.w-100.w-third-l.pa1.i', field.description),
    ),
}

const Schema = {
    view: ({ attrs: { fields } }) => m(
        '.pa1.pa3-l.mv2.ba.b--black-10.shadow-4',
        [ 'field', 'type', 'description' ].map(heading => m(
            '.fl.w-100.w-third-l.f4.f3-l.dn.db-l.ph1.bb.b--silver',
            heading,
        )),
        fields.map((field, i) => m(
            SchemaRow, { field, isLast: (i === fields.length - 1) }
        )),
    ),
}

const EndpointDescription = {
    view: ({ children, attrs: { url, description, fields, type } }) => [
        m('.f4.f3-l.code', url),
        m('.i.f7.f6-l', description),
        m('.small-caps', type),
        children,
    ],
}

function sumArray(array) {
    if (array.length === 0) { return 0; }

    return array.reduce((a, b) => a + b);
}

function sumLogRequests(datetimes) {
    const allCounts = datetimes
        .map(d => log_provider.getLog(d.toISO()))
        .filter(res => res.status === 'SUCCESS')
        .map(res => res.value)
        .flat()
        .map(([kanji, count]) => count)
    return sumArray(allCounts)
}

function collateLogRequests(datetimes) {
    const allResults = datetimes
        .map(d => log_provider.getLog(d.toISO()))
        .filter(res => res.status === 'SUCCESS')
        .map(res => res.value)
        .flat();

    const countByKanji = allResults
        .reduce((acc, [kanji, n]) => {
            let count = acc[kanji];
            if (count === undefined) count = 0;
            acc[kanji] = count+n;
            return acc;
        }, {});

    const sorted = Object.entries(countByKanji).sort((a, b) => b[1] - a[1]);
    return sorted;
}

const TotalPopularityByDay = {
    view: () => {
        const today = DateTime.utc().startOf('day')
        const previous_seven_days_hours = [...Array(7).keys()]
            .map(i => today.minus({days: 7-i}))
            .map(d => [...Array(24).keys()].map(i => d.plus({hours: i})))

        const previous_seven_days_flat = previous_seven_days_hours.flat()

        return m(
            '.ma3',
            previous_seven_days_hours.map(datetimes => [
                m('.fl.w-50.tr.pr3', datetimes[0].toLocaleString(DateTime.DATE_SHORT)),
                m('.fl.w-50', sumLogRequests(datetimes).toLocaleString()),
            ]),
            [
                m('.fl.w-50.tr.pr3.vermillion', 'Total',),
                m('.fl.w-50.vermillion', sumLogRequests(previous_seven_days_flat).toLocaleString()),
            ],
        )
    },
}

const LogsDashboard = {
    view: () => [
        m(
            '.self-center.mv2.tc.underline',
            m(InternalLink, { href: '/' }, 'home'),
        ),
        m(
            '.mh3',
            [
                'These logs show how many times ',
                m('span.vermillion', '/kanji/{character}'),
                ' and ',
                m('span.vermillion', '/kanji/{list}'),
                ' endpoints were served successfully in the last 7 days (there is a lag on logs coming through, so the last 24-48 hours may show less than the final total)',
            ],
        ),
        m(TotalPopularityByDay),
        m(KanjiPopularity),
    ],
}

const Docs = {
    view: () => [
        m(
            '.self-center.mv2.tc.underline',
            m(InternalLink, { href: '/' }, 'home'),
        ),
        m(
            EndpointDescription,
            {
                url: 'GET /v1/kanji/{list}',
                type: 'string[]',
                description: [
                    'Provides lists of kanji by category (see ',
                    m(Link, { href: README_URL }, 'README'),
                    ' for detailed information on which characters are in which list)',
                ],
            },
            m(
                '.pa1.pa3-l.mv2.ba.b--black-10.shadow-4',
                KANJI_LIST_ENDPOINTS.map((endpoint, i) => m(
                    KanjiListEndpoint,
                    {
                        endpoint,
                        isLast: (i === KANJI_LIST_ENDPOINTS.length - 1),
                    },
                )),
            ),
        ),
        m(Separator),
        m(
            EndpointDescription,
            {
                url: 'GET /v1/kanji/{character}',
                type: 'kanji',
                description: 'Provides general information about the supplied kanji character',
            },
            m(Schema, { fields: KANJI_FIELDS }),
        ),
        m(Separator),
        m(
            EndpointDescription,
            {
                url: 'GET /v1/reading/{reading}',
                type: 'reading',
                description: 'Provides lists of kanji associated with the supplied reading',
            },
            m(Schema, { fields: READING_FIELDS }),
        ),
        m(Separator),
        m(
            EndpointDescription,
            {
                url: 'GET /v1/words/{character}',
                type: 'word[]',
                description: 'Provides a list of dictionary entries associated with the supplied kanji character',
            },
            m('.small-caps.mt3', 'word'),
            m(Schema, { fields: WORD_FIELDS }),
            m('.small-caps', 'meaning'),
            m(Schema, { fields: MEANING_FIELDS }),
            m('.small-caps', 'variant'),
            m(Schema, { fields: VARIANT_FIELDS }),
        ),
    ]
}

function Home() {
    let path = stream('kanji/蛍')

    return {
        view: ({ attrs: { kanjiapi } }) => [
            m('.self-center.mv2.f4.f3-l.tc', 'A modern JSON API for kanji'),
            m(
                '.self-center.mv2.tc.underline',
                m(InternalLink, { href: '/documentation' }, 'documentation'),
            ),
            m(
                '.self-center.mv2.tc.underline',
                m(InternalLink, { href: '/logs' }, 'logs dashboard'),
            ),
            m(
                '.self-center.mv2.tc.underline',
                m(
                    Link,
                    { href: KANJIAPI_WRAPPER_URL },
                    'official wrapper library',
                ),
            ),
            m('.self-center.mv2.tc.underline', m(
                Link,
                { href: 'kanjiapi_full.zip' },
                'API data download',
            )),
            m(Separator),
            m('.mv1.self-start', 'Try it!'),
            m(Search, { path }),
            m(Examples, { path }),
            m('.mv1.self-start', 'Resource:'),
            m(SearchResult, { result: kanjiapi.getUrl(`/${path()}`) }),
            m(Separator),
            m(About),
        ],
    }
}

const Page = {
    view: ({ children }) => [
        m(Header),
        m(
            '.f5.flex.flex-column.items-stretch.flex-auto.pv3.ph2.w-70-l.lh-copy',
            children,
        ),
        m(Footer),
    ]
}

m.route(document.body, '/', {
    '/': { render: () => m(Page, m(Home, { kanjiapi })) },
    '/documentation': { render: () => m(Page, m(Docs)) },
    '/logs': { render: () => m(Page, m(LogsDashboard)) },
})
