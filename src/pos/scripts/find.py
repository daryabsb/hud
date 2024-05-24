word_list = ["chrome", "firefox", "codepen", "javascript", "jquery", "twitter", "github", "wordpress", "opera", "sass", "layout", "standards", "semantic", "designer", "developer", "module", "component", "website", "creative", "banner", "browser", "screen", "mobile", "footer", "header", "typography", "responsive", "programmer", "css", "border", "compass", "grunt", "pixel", "document", "object", "ruby", "modernizr",
             "bootstrap", "python", "php", "pattern", "ajax", "node", "element", "android", "application", "adobe", "apple", "google", "microsoft", "bookmark", "internet", "icon", "svg", "background", "property", "syntax", "flash", "html", "font", "blog", "network", "server", "content", "database", "socket", "function", "variable", "link", "apache", "query", "proxy", "backbone", "angular", "email", "underscore", "cloud"]


def run():
    three_words = ['css', 'php', 'svg']
    four_words = ['sass', 'ruby', 'ajax', 'node',
                  'icon', 'html', 'font', 'blog', 'link']

    five_words = ['opera', 'grunt', 'pixel', 'adobe',
                  'apple', 'flash', 'query', 'proxy', 'email', 'cloud']

    six_words = ['chrome', 'jquery', 'github', 'layout', 'module', 'banner',
                 'screen', 'mobile', 'footer', 'header', 'border', 'object',
                 'python', 'google', 'syntax', 'server', 'socket', 'apache']

    seven_words = ['firefox', 'codepen', 'twitter', 'website', 'browser',
                   'compass', 'pattern', 'element', 'android', 'network',
                   'content', 'angular']

    eight_words = ['semantic', 'designer', 'creative', 'document', 'bookmark',
                   'internet', 'property', 'database', 'function', 'variable',
                   'backbone']
    nine_words = ['wordpress', 'standards', 'developer',
                  'component', 'modernizr', 'bootstrap', 'microsoft']

    ten_words = ['javascript', 'typography', 'responsive',
                 'programmer', 'background', 'underscore']

    eleven_words = ['application']

    no_e = ['javascript', 'github', 'sass', 'layout', 'standards', 'typography', 'css', 'compass', 'grunt', 'ruby', 'bootstrap', 'python', 'php', 'ajax', 'android',
            'application', 'microsoft', 'bookmark', 'icon', 'svg', 'background', 'syntax', 'flash', 'html', 'font', 'blog', 'function', 'link', 'proxy', 'angular', 'cloud']
    no_o = ['javascript', 'jquery', 'twitter', 'github', 'sass', 'standards', 'semantic', 'designer', 'website', 'creative', 'banner', 'screen', 'header', 'css', 'grunt', 'pixel',
            'ruby', 'php', 'pattern', 'ajax', 'element', 'apple', 'internet', 'svg', 'syntax', 'flash', 'html', 'server', 'database', 'variable', 'link', 'apache', 'query', 'angular', 'email']
    no_a = ['chrome', 'firefox', 'codepen', 'jquery', 'twitter', 'github', 'wordpress', 'designer', 'developer', 'module',
            'component', 'website', 'browser', 'screen', 'mobile', 'footer', 'responsive', 'css', 'border', 'grunt', 'pixel',
            'document', 'object', 'ruby', 'modernizr', 'python', 'php', 'node', 'element',
            'google', 'microsoft', 'internet', 'icon', 'svg', 'property', 'html', 'font',
            'blog', 'network', 'server', 'content', 'socket', 'function', 'link', 'query',
            'proxy', 'underscore', 'cloud']
    no_i = ['chrome', 'codepen', 'jquery', 'wordpress', 'opera', 'sass', 'layout', 'standards', 'developer', 'module', 'component', 'banner', 'browser', 'screen', 'footer', 'header', 'typography', 'programmer', 'css', 'border', 'compass', 'grunt', 'document', 'object', 'ruby', 'bootstrap', 'python',
            'php', 'pattern', 'ajax', 'node', 'element', 'adobe', 'apple', 'google', 'bookmark', 'svg', 'background', 'property', 'syntax', 'flash', 'html', 'font', 'blog', 'network', 'server', 'content', 'database', 'socket', 'apache', 'query', 'proxy', 'backbone', 'angular', 'underscore', 'cloud']
    no_s = []
    no_y = []
    twelve_words = []
    for word in word_list:
        if len(word) == 12:
            twelve_words.append(word)
        else:
            continue
    print(twelve_words)
