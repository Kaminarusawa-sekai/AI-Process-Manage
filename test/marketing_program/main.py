import user_portrait_initial
import Identify_competitors
import economic_analysis
import political_and_regulatory_analysis
import enterprise_characteristic_analysis
import enterprises_competitiveness_analysis
import enterprise_strategic_vision_long


product_content='''
        中科蓝吧数字科技（苏州）有限公司是一家AI企服领域的科创型企业。公司以AI为核心驱动力，通过行业化AI模型、场景化AI能力，为企业量身打造高效、智能的AI转型升级方案，为企业降本增效、全新发展注入强劲的AI动能。
        我们的产品是一款面向中小企业的云端企业服务管理软件，主要功能包括营销管理和经营分析，以及一些业务辅助功能。
'''


user_portrait_initiasl_word=user_portrait_initial.get_user_portrait_initial(product_content)


identify_competitors_word=Identify_competitors.get_identify_compeitors(user_portrait_initiasl_word)
economic_analysis_word=economic_analysis.get_economic_analysis(user_portrait_initiasl_word)
political_and_regulatory_analysis_word=political_and_regulatory_analysis.get_political_and_regulatory_analysis(user_portrait_initiasl_word)

enterprise_characteristic_analysis_word=enterprise_characteristic_analysis.get_enterprise_characteristic_analysis(product_content)
enterprises_competitiveness_analysis_word=enterprises_competitiveness_analysis.get_enterprise_competitiveness_analysis(enterprise_characteristic_analysis_word)

enterprise_strategic_vision_long_word=enterprise_strategic_vision_long.get_enterprise_strategic_vision_long(identify_competitors_word,economic_analysis_word,political_and_regulatory_analysis_word,enterprise_characteristic_analysis_word,enterprises_competitiveness_analysis_word)



