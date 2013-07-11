from five import grok
from plone.directives import dexterity, form
from wcc.homepage.content.homepage3 import IHomepage3

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IHomepage3)
    grok.require('zope2.View')
    grok.template('homepage3_view')
    grok.name('view')

    def news_items(self):
        rel = self.context.news_source
        if not rel:
            return []
        source = rel.to_object
        results = source.queryCatalog(batch=False) or []
        count = 2 if self.thirdcolumn() else 3
        return [i.getObject() for i in results[:count]]

    def more_news_target(self):
        if self.context.more_news_target:
            return self.context.more_news_target.to_object
        if self.context.news_source:
            return self.context.news_source.to_object
        return None

    def slider_items(self):
        if not self.context.slider_items:
            return []
        return [i.to_object for i in self.context.slider_items]

    def get_image_tag(self, obj):
        scales = obj.restrictedTraverse('@@images')
        image = scales.scale('carousel_image', width=510, height=330)
        placeholder = '<img src="http://placehold.it/510x330"/>'
        if not image:
            return placeholder
        return image.tag()

    def thirdcolumn(self):
        return (self.context.third_column_text or '').strip()

    def newsblock_class(self, index, count):
        if index == 0:
            return "cell width-1:%s position-0" % count
        return "cell width-1:%s position-%s:%s" % (count, index, count)

class HomepageJS(grok.View):
    grok.context(IHomepage3)
    grok.name('homepage.js')

    def render(self):
        self.request.response.setHeader('Content-Type', 'text/javascript')
        template = '''
var homepageJQ = $.noConflict();
homepageJQ(document).ready(function() {
    homepageJQ("#homepage-slider").lofJSidernews({ interval:5000,
        easing:'easeInOutQuad',
        duration:600,
        direction: 'opacity',
        auto:true,
        mainWidth:%(width)s,
        mainHeight:%(height)s,
        navigatorHeight : 87,
        navigatorWidth : 303,
        maxItemDisplay:4,
        navigatorEvent: 'mouseenter'
    });
})
        '''

        return template % {'width': 510, 'height': 330}

