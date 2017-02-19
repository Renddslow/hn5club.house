import random
import models


class Corporate:
	def __init__(self, bs_creator):
		self.adverbs = ["appropriately","assertively","authoritatively",
						"collaboratively","compellingly","competently",
						"completely","continually","conveniently","credibly",
						"distinctively","dramatically","dynamically",
						"efficiently","energistically","enthusiastically",
						"fungibly","globally","holisticly","interactively",
						"intrinsically","monotonectally","objectively",
						"phosfluorescently","proactively","professionally",
						"progressively","quickly","rapidiously","seamlessly",
						"synergistically","uniquely"]
		self.verbs = ["actualize","administrate","aggregate",
						"architect","benchmark","brand","build",
						"cloudify","communicate","conceptualize",
						"coordinate","create","cultivate","customize",
						"deliver","deploy","develop","dinintermediate disseminate",
						"drive","embrace","e-enable","empower","enable","engage",
						"engineer","enhance","envisioneer","evisculate","evolve",
						"expedite","exploit","extend","fabricate","facilitate",
						"fashion","formulate","foster","generate","grow","harness",
						"impact","implement","incentivize","incubate","initiate",
						"innovate","integrate","iterate","leverage existing",
						"leverage other's","maintain","matrix","maximize","mesh",
						"monetize","morph","myocardinate","negotiate","network",
						"optimize","orchestrate","parallel task","plagiarize",
						"pontificate","predominate","procrastinate","productivate",
						"productize","promote","provide access to","pursue",
						"recaptiualize","reconceptualize","redefine","re-engineer",
						"reintermediate","reinvent","repurpose","restore",
						"revolutionize","right-shore","scale","seize","simplify",
						"strategize","streamline","supply","syndicate","synergize",
						"synthesize","target","transform","transition","underwhelm",
						"unleash","utilize","visualize","whiteboard"]
		self.adjectives = ["24/7","24/365","accurate","adaptive","alternative","an expanded array of",
							"B2B","B2C","backend","backward-compatible","best-of-breed","bleeding-edge",
							"bricks-and-clicks","business","clicks-and-mortar","client-based","client-centered",
							"clientcentric","client-focused","cloud-based","cloud-centric","cloudified",
							"collaborative","compelling","competitive","cooperative","corporate",
							"cost effective","covalent","cross functional","cross-media","cross-platform",
							"cross-unit","customerdirected","customized","cutting-edge","distinctive",
							"distributed","diverse","dynamic","e-business","economically sound",
							"effective","efficient","elastic","emerging","empowered","enabled","end-to-end",
							"enterprise","enterprise-wide","equityinvested","error-free","ethical","excellent",
							"exceptional","extensible","extensive","flexible","focused","frictionless",
							"front-end","fully researched","fully tested","functional","functionalized",
							"fungible","future-proof","global","goforward","goal-oriented","granular",
							"high standards in","high-payoff","hyperscale","high-quality","highly efficient",
							"holistic","impactful","inexpensive","innovative","installedbase","integrated",
							"interactive","interdependent","intermandated","interoperable","intuitive",
							"just in time","leading-edge","leveraged","long-term high-impact",
							"low-risk high-yield","magnetic","maintainable","market positioning",
							"marketdriven","mission-critical","multidisciplinary","multifunctional",
							"multimedia based","next-generation","on-demand","one-to-one","open-source",
							"optimal","orthogonal","out-of-the-box","pandemic","parallel","performance based",
							"plug-andplay","premier","premium","principle-centered","proactive",
							"process-centric","professional","progressive","prospective","quality","real-time",
							"reliable","resource-sucking","resource-maximizing","resourceleveling",
							"revolutionary","robust","scalable","seamless","stand-alone","standardized",
							"standards compliant","state of the art","sticky","strategic","superior",
							"sustainable","synergistic","tactical","team building","team driven",
							"technicallysound","timely","top-line","transparent","turnkey","ubiquitous",
							"unique","user-centric","user friendly","value-added","vertical","viral",
							"virtual","visionary","web-enabled","wireless","world-class","worldwide"]
		self.nouns = ["action items","alignments","applications","architectures",
						"bandwidth","benefits","best practices","catalysts for change",
						"channels","clouds","collaboration and idea-sharing",
						"communities","content","convergence","core competencies",
						"customer service","data","deliverables","e-business",
						"e-commerce","e-markets","e-tailers","e-services",
						"experiences","expertise","functionalities","fungibility",
						"growth strategies","human capital","ideas","imperatives",
						"infomediaries","information","infrastructures","initiatives",
						"innovation","intellectual capital","interfaces",
						"internal or \"organic\" sources","leadership","leadership skills",
						"manufactured products","markets","materials","meta-services",
						"methodologies","methods of empowerment","metrics","mindshare",
						"models","networks","niches","niche markets","nosql",
						"opportunities","\"outside the box\" thinking","outsourcing",
						"paradigms","partnerships","platforms","portals",
						"potentialities","rocess improvements","processes","products",
						"quality vectors","relationships","resources","results","ROI",
						"scenarios","schemas","services","solutions","sources",
						"strategic theme areas","storage","supply chains","synergy",
						"systems","technologies","technology","testing procedures",
						"total linkage","users","value","vortals","web-readiness",
						"web services","virtualization"]
		self.indexes = {
			"adverbs": random.randrange(len(self.adverbs)),
			"verbs": random.randrange(len(self.verbs)),
			"adjectives": random.randrange(len(self.adjectives)),
			"nouns": random.randrange(len(self.nouns))
		}
		self.bs_creator = bs_creator

	
	def create_corporate_bs(self):
		bs = "We need to {} {} {} {}".format(
			self.adverbs[self.indexes["adverbs"]],
			self.verbs[self.indexes["verbs"]],
			self.adjectives[self.indexes["adjectives"]],
			self.nouns[self.indexes["nouns"]]
		)
		self.log_bs(bs)
		return bs


	def log_bs(self, bs):
		indexes = "{}:{}:{}:{}".format(
			self.adverbs[self.indexes["adverbs"]],
            self.verbs[self.indexes["verbs"]],
            self.adjectives[self.indexes["adjectives"]],
            self.nouns[self.indexes["nouns"]]
		)
		models.BS.create(bs_phrase = bs, bs_index = indexes, 
						bs_creator = self.bs_creator)
