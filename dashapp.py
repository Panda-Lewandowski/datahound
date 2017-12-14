import dash
import dash_core_components as dcc
import dash_html_components as html

import community as cm
import views as vws
import settings as st
import exceptions as exc


class CommunityAnalysisApp:
    def __init__(self, name="thevillage", debug=True, start=True):
        self.debug = debug
        self.community_name = name
        self.app = dash.Dash()
        self.public = None
        if start:
            self._start()

    def _start(self):
        if self.debug:
                print("Just start app.")

        self.public = cm.Community(self.community_name)

        if self.debug:
            print("We got info of community")

        self.public.display()

    def get_diagrams(self):
        if self.debug:
            print("Okey, we got some data. Start to visualize...")
        sex_pie = vws.pie_chart(self.public.sex_data(), st.SEX_COLORS, 'Sex')

        funnel = vws.funnel(["Views", "Likes", 'Reposts'], self.public.likes_data())

        plat_data, sys_data = self.public.platform_data()

        ad_data = self.public.ad_ratio()

        # print(plat_data.keys())
        
        platform_pie = vws.pie_chart(plat_data, ['#66CDAA', '#EE5C42', '#B22222', '#1874CD'], 'Platform')
        system_pie = vws.pie_chart(sys_data, st.SYSTEM_COLORS, 'System')

        ages_female, xbins_female, ages_male, xbins_male, ukn = self.public.age_data()

        gist_female = vws.histogram(ages_female, xbins_female, st.SEX_COLORS[0], 'Female')
        gist_male = vws.histogram(ages_male, xbins_male, st.SEX_COLORS[1], 'Male')

        max_age = max(xbins_female['end'], xbins_male['end'])
        step = xbins_female['size']
        labels = ['\t\t\t\t\t\t\t\t\t\t\t\t {0} - {1} \t\t\t\t\t\t\t\t\t\t\t\t '.format(a, a + step) for a in range(0, max_age + step, step)]
        values = [a for a in range(0, max_age + step, step)]

        lay = vws.layout('Sex/Age', labels, values, 'Age ({0} Uknown)'.format(ukn), 'Amount')

        fig_sex_age = vws.store_2_fig(gist_female, gist_male, lay)

        ad_ratio = vws.pie_chart(ad_data, st.SYSTEM_COLORS, 'Ad ratio')

        # TODO divide it to generate_data() and generate_html()

        self.app.layout = html.Div(children=[
            html.H1(children='Analisys of {0}'.format(self.community_name)),

            dcc.Graph(id='Sex', figure={'data': sex_pie}),

            dcc.Graph(id='Likes funnel', figure={'data': funnel[0], 'layout': funnel[1]}),

            dcc.Graph(id='Plaform', figure={'data': platform_pie}),

            dcc.Graph(id='System', figure={'data': system_pie}),

            dcc.Graph(id='Ages', figure={'data': fig_sex_age}),

            dcc.Graph(id='Ad ratio', figure={'data': ad_ratio})

        ])

    def run(self):
        self.get_diagrams()

        if self.debug:
            print("We draw this awesome graph, bro. Check it.")

        self.app.run_server(port=8080)


if __name__ == '__main__':
    try:
        pub = CommunityAnalysisApp(start=True)
        pub.run()
    except exc.VkAPIError:
        print('Oops, get token, please')



