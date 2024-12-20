## 这些部分是分析企业战略愿景的
import user_portrait_initial 
import Identify_competitors
import economic_analysis
import political_and_regulatory_analysis
import enterprise_characteristic_analysis
import enterprises_competitiveness_analysis
import enterprise_strategic_vision_long

## 这些部分是分析企业营销形象的
import determine_customer_targeting
import Identify_customer_interests
import Identify_enterprise_image

## 这些部分是分析Boss营销形象的
import boss_characteristic_identify
import boss_enterprise_characteistic_identify

import generate_marketing_program

import generate_promotional_stories
import generate_stories_styies


product_content='''
        中科蓝吧数字科技（苏州）有限公司是一家AI企服领域的科创型企业。公司以AI为核心驱动力，通过行业化AI模型、场景化AI能力，为企业量身打造高效、智能的AI转型升级方案，为企业降本增效、全新发展注入强劲的AI动能。
        我们的产品是一款面向中小企业的云端企业服务管理软件，主要功能包括营销管理和经营分析，以及一些业务辅助功能。
'''

Boss_MBTI='INFJ'
BOSS_strengths='企业主的性格特点是坚持'


user_portrait_initiasl_word=user_portrait_initial.get_user_portrait_initial(product_content)


identify_competitors_word=Identify_competitors.get_identify_compeitors(user_portrait_initiasl_word)
economic_analysis_word=economic_analysis.get_economic_analysis(user_portrait_initiasl_word)
political_and_regulatory_analysis_word=political_and_regulatory_analysis.get_political_and_regulatory_analysis(user_portrait_initiasl_word)

enterprise_characteristic_analysis_word=enterprise_characteristic_analysis.get_enterprise_characteristic_analysis(product_content)
enterprises_competitiveness_analysis_word=enterprises_competitiveness_analysis.get_enterprise_competitiveness_analysis(enterprise_characteristic_analysis_word)

enterprise_strategic_vision_long_word=enterprise_strategic_vision_long.get_enterprise_strategic_vision_long(identify_competitors_word,economic_analysis_word,political_and_regulatory_analysis_word,enterprise_characteristic_analysis_word,enterprises_competitiveness_analysis_word)

determine_customer_targeting_word=determine_customer_targeting.get_customer_targeting(enterprise_strategic_vision_long_word)
Identify_customer_interests_word=Identify_customer_interests.get_custom_interst(determine_customer_targeting_word)
Identify_enterprise_image_word=Identify_enterprise_image.get_enterprise_image(Identify_customer_interests_word)

boss_characteristic_identify_word=boss_characteristic_identify.get_boss_characteristic(Boss_MBTI,BOSS_strengths)
boss_enterprise_characteistic_identify_word=boss_enterprise_characteistic_identify.get_boss_enterprise_characteristic(boss_characteristic_identify_word)

generate_marketing_program_word=generate_marketing_program.get_marketing_program(enterprise_strategic_vision_long_word,Identify_enterprise_image_word,boss_enterprise_characteistic_identify_word)

generate_promotional_stories_word=generate_promotional_stories.get_promotional_stories(generate_marketing_program_word)
generate_stories_styies_word=generate_stories_styies.get_stories_styles(generate_promotional_stories_word)



