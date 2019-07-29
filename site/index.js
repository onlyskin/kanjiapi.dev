const m = require('mithril')
const stream = require('mithril/stream')
const { Kanjiapi } = require('kanjiapi-wrapper')

const NOT_FOUND = 'Not Found'
const LOADING = 'Loading'

const kanjiapi = Kanjiapi.build(m.redraw)

const Link = {
    view: ({ children, attrs: { href } }) => m('a.vermillion', { href }, children),
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
        ]
    )
}

const Footer = {
    view: () => m(
        '',
        { style: { 'height': '50px' } },
        m(Link, { href: 'https://github.com/onlyskin/kanjiapi.dev' }, m(GithubIcon)),
    )
}

const Header = {
    view: () => m(
        '.border-box.pa2.pa3-ns.white.w-100.bg-dark-ink',
        [ m('.tc.ma1.f2.f1-ns.rounded', '漢字'), m('.tc.ma1.f2.f1-ns', 'kanjiapi.dev') ],
    )
}

const About = {
    view: () => [
        m('.f4.b.tc.mv2.nowrap', 'What is this?'),
        m(
            '.self-start.pv2',
            'This is an API that provides JSON endpoints for over 13,000 ',
            m(Link, { href: 'https://en.wikipedia.org/wiki/Kanji' }, 'kanji'),
            ' using data from an extensive kanji dictionary.'
        ),
        m(
            '.self-start.pv2',
            'This API uses the EDICT and KANJIDIC dictionary files. ',
            'These files are the property of the ',
            m(Link, { href: 'http://www.edrdg.org/' },
                'Electronic Dictionary Research and Development Group'),
            ', and are used in conformance with the Group\'s ',
            m(Link, { href: 'http://www.edrdg.org/edrdg/licence.html' },
                'licence'),
            '.',
        ),
        m(
            '.self-start.pv2',
            'This page is built using ',
            m(Link, { href: 'https://mithril.js.org/' }, 'mithril.js'),
            '.',
        ),
    ]
}

const Separator = {
    view: () => m('hr.w-100.black-50.mv3')
}

const Search = {
    view: ({ attrs: { path } }) => m(
        '.w-100.flex.items-stretch.mt1.mb0',
        [
            m('label#search-label', 'https://kanjiapi.dev/v1/'),
            m(
                'input[type=text]#search-input',
                {
                    value: path(),
                    onchange: e => path(e.target.value),
                },
            ),
        ],
    ),
}

const Example = {
    view: ({ attrs: { path, url } }) => m(
        '.di.i.underline.nowrap.vermillion',
        { onclick: () => path(url) },
        url,
    )
}

const Examples = {
    view: ({ attrs: { path } }) => m(
        '.f7.f6-ns.self-start.mt0.mb1',
        [
            'Hint: try ',
            m(Example, { path, url: 'kanji/蜜' }),
            ', ',
            m(Example, { path, url: 'kanji/grade-1' }),
            ', ',
            m(Example, { path, url: 'reading/あり' }),
            ', or ',
            m(Example, { path, url: 'words/蠍' }),
        ],
    ),
}

const SearchResult = {
    view: ({ attrs: { url } }) => m(
        '.self-stretch.f7.f6-ns.pa1.pa2-ns.mv1.ba.b--black-10.border-box.shadow-4.code.pre.pre-wrap',
        kanjiapi.getUrl(`/${url}`).status === Kanjiapi.SUCCESS ?
        JSON.stringify(kanjiapi.getUrl(`/${url}`).value, null, 2) :
        kanjiapi.getUrl(`/${url}`).status === Kanjiapi.LOADING ? 'Loading' :
        kanjiapi.getUrl(`/${url}`).status === Kanjiapi.ERROR ? 'Not Found' : 'Error',
    ),
}

const KANJI_FIELDS = [
    { name: 'kanji', description: 'The kanji itself', type: 'string' },
    {
        name: 'grade',
        description: [
            'The official grade of the kanji (1-6 for ',
            m(Link, { href: 'https://en.wikipedia.org/wiki/Ky%C5%8Diku_kanji' }, 'Kyōiku kanji'),
            ', 8 for the remaining ',
            m(Link, { href: 'https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji' }, 'Jōyō kanji'),
            ', 9/10 for ',
            m(Link, { href: 'https://en.wikipedia.org/wiki/Jinmeiy%C5%8D_kanji' }, 'Jinmeiyō kanji'),
            ')',
        ],
        type: 'number',
    },
    {
        name: 'stroke_count',
        description: 'The number of strokes necessary to write the kanji',
        type: 'number'
    },
    {
        name: 'meanings',
        description: 'A list of English meanings associated with the kanji',
        type: 'string[]'
    },
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
        name: 'jlpt',
        description: [
            'The former ',
            m(Link, { href: 'https://en.wikipedia.org/wiki/Japanese-Language_Proficiency_Test' }, 'JLPT'),
            ' test level for the kanji',
        ],
        type: 'number',
    },
    {
        name: 'unicode',
        description: [
            'The ',
            m(Link, { href: 'https://en.wikipedia.org/wiki/Unicode' }, 'Unicode'),
            ' codepoint of the kanji',
        ],
        type: 'string',
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

const SchemaRow = {
    view: ({ attrs: { field, isLast } }) => m('.cf.pv2.pv0-ns.bb.b--silver', [
        m(
            '.fl.w-50.w-third-ns.pa1.code',
            `"${field.name}":`,
        ),
        m(
            '.fl.w-50.w-third-ns.pa1.code.small-caps.tr.tl-ns',
            field.type,
        ),
        m(
            '.f7.f6-ns.fl.w-100.w-third-ns.pa1.i',
            field.description,
        ),
    ]),
}

const Schema = {
    view: ({ attrs: { fields } }) => m(
        '.pa1.pa3-ns.mv2.ba.b--black-10.shadow-4',
        [ 'field', 'type', 'description' ].map(heading => m('.fl.w-100.w-third-ns.b.dn.db-ns.ph1.bb.b--silver', heading)),
        fields.map((field, i) => m(SchemaRow, { field, isLast: (i === fields.length - 1) })),
    ),
}

const EndpointDescription = {
    view: ({ children, attrs: { url, description, fields, type } }) => [
        m('.f3', url),
        m('.i.f7.f6-ns', description),
        m('.small-caps', type),
        children,
    ],
}

const Docs = {
    view: () => [
        m('.self-center.mv2.tc.underline', m(m.route.Link, { href: '/', class: 'vermillion' }, 'home')),
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
        view: () => [
            m('.self-center.mv2.b.tc', 'A modern JSON API for kanji'),
            m('.self-center.mv2.tc.underline', m(
                m.route.Link,
                { href: '/documentation', class: 'vermillion' },
                'documentation'),
            ),
            m(
                '.self-center.mv2.tc',
                'Check out ',
                m(Link, { href: 'https://kai.kanjiapi.dev' }, 'kanjikai'),
                ', a webapp powered by kanjiapi.dev',
            ),
            m(Separator),
            m('.mv1.self-start', 'Try it!'),
            m(Search, { path }),
            m(Examples, { path }),
            m('.mv1.self-start', 'Resource:'),
            m(SearchResult, { url: path() }),
            m(Separator),
            m(About),
        ],
    }
}

const Page = {
    view: ({ children }) => [
        m(Header),
        m(
            '.f5.flex.flex-column.items-stretch.flex-auto.pv3.ph2.w-80-m.w-70-l.lh-copy',
            children,
        ),
        m(Footer),
    ]
}

m.route(document.body, '/', {
    '/': { render: () => m(Page, m(Home)) },
    '/documentation': { render: () => m(Page, m(Docs)) },
})
