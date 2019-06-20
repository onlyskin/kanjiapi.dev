const m = require('mithril')

const NOT_FOUND = 'Not Found'

const globalInputState = {
    value: null,
    response: null,
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
        m('a.black[href=https://github.com/onlyskin/kanjiapi.dev]', m(GithubIcon),
        ),
    )
}

const Header = {
    view: () => m(
        '.border-box.pa2.pa3-ns.white.w-100.flex.flex-column.items-center.bg-dark-ink',
        [ m('.ma1.f2.f1-ns.rounded', '漢字'), m('.ma1.f2.f1-ns', 'kanjiapi.dev') ],
    )
}

const About = {
    view: () => [
        m('.f4.b.mv2.nowrap', 'What is this?'),
        m(
            '.self-start.lh-copy.pv2',
            'This is an API that provides JSON endpoints for over 13,000 ',
            m('a.black[href=https://en.wikipedia.org/wiki/Kanji]', 'Kanji'),
            ' using data from an extensive Kanji dictionary.'
        ),
        m(
            '.self-start.lh-copy.pv2',
            'This API uses the EDICT and KANJIDIC dictionary files. ',
            'These files are the property of the ',
            m(
                'a.black[href=http://www.edrdg.org/]',
                'Electronic Dictionary Research and Development Group'
            ),
            ', and are used in conformance with the Group\'s ',
            m(
                'a.black[href=http://www.edrdg.org/edrdg/licence.html]',
                'licence'
            ),
            '.',
        ),
        m(
            '.self-start.lh-copy.pv2',
            'This page is built using ',
            m('a.black[href=https://mithril.js.org/]', 'mithril.js'),
            '.',
        ),
    ]
}

function updateInput(url) {
    globalInputState.value = url

    return m.request({
        url: `https://kanjiapi.dev/${url}`,
    })
        .then(response => {
            globalInputState.value = url
            globalInputState.response = response
        })
        .catch(error => {
            globalInputState.value = url
            globalInputState.response = NOT_FOUND
        })
}

const Example = {
    view: ({ attrs: { url } }) => m(
        '.di.code.underline',
        {
            onclick: _ => updateInput(url),
        },
        url,
    )
}

const Separator = {
    view: () => m('hr.w-100.black-50.ma3')
}

const Page = {
    oninit: () => updateInput('v1/kanji/蛍'),
    view: () => [
        m(Header),
        m(
            '.flex.flex-column.items-center.flex-auto.pv3.ph2.w-70-ns.lh-copy',
            [
                m('.mv2.b', 'A modern JSON API for Kanji'),
                m('.mv2.tc', 'Check out ', m('a[href=https://kai.kanjiapi.dev].black', 'kanjikai'), ', a webapp powered by kanjiapi.dev'),
                m(Separator),
                m('.self-start.f4', 'Try it!'),
                m(
                    '#api-test-url',
                    [
                        m('label[for=url-input]', 'https://kanjiapi.dev/'),
                        m(
                            'input#url-input[type=text]',
                            {
                                value: globalInputState.value,
                                onchange: e => {
                                    updateInput(e.target.value)
                                },
                            },
                        )
                    ],
                ),
                m(
                    '.self-start.mv2',
                    [
                        'Try ',
                        m(Example, { url: 'v1/kanji/蜜' }),
                        ', ',
                        m(Example, { url: 'v1/kanji/grade-1' }),
                        ', ',
                        m(Example, { url: 'v1/reading/あり' }),
                        ', or ',
                        m(Example, { url: 'v1/words/蠍' }),
                    ],
                ),
                m('.self-start', 'Resource:'),
                m(
                    '.w-100.lh-copy.pa3.mv2.ba.b--black-10.border-box.shadow-4.pre.code#api-reponse',
                    globalInputState.response ?
                    globalInputState.response === NOT_FOUND ?
                    'Not Found' :
                    JSON.stringify(globalInputState.response, null, 2) :
                    'Loading',
                ),
                m(Separator),
                m(About),
            ]
        ),
        m(Footer),
    ]
}

m.mount(document.body, Page)
