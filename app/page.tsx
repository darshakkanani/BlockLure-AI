'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { 
  Shield, 
  CheckCircle, 
  Zap, 
  Brain, 
  Lock, 
  Users, 
  Globe, 
  BarChart3, 
  Target, 
  Activity, 
  TrendingUp, 
  Eye, 
  ArrowRight, 
  Play
} from 'lucide-react'

const features = [
  {
    icon: Eye,
    title: 'Smart Detection',
    description: 'AI-powered threat detection that learns and adapts',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: Brain,
    title: 'Real-time Analysis',
    description: 'Instant threat analysis with machine learning',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Shield,
    title: 'Automated Defense',
    description: 'Automatic response to cyber threats',
    color: 'from-green-500 to-emerald-500'
  }
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-32">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-6xl md:text-8xl font-bold text-white mb-8">
                <span className="bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                  BlockLure AI
                </span>
              </h1>
              <p className="text-2xl md:text-3xl text-gray-300 mb-6">
                Smart Cyber Defense System
              </p>
              <p className="text-xl text-gray-400 max-w-3xl mx-auto mb-12 leading-relaxed">
                AI-powered threat detection that learns, adapts, and protects your systems automatically
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-6 justify-center"
            >
              <Link href="/dashboard" className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl inline-flex items-center space-x-3">
                <Shield className="w-6 h-6" />
                <span>View Dashboard</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link href="/features" className="bg-white/10 backdrop-blur-sm text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/20 transition-all duration-300 border border-white/20 inline-flex items-center space-x-3">
                <Play className="w-5 h-5" />
                <span>Learn More</span>
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white/5 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Why Choose BlockLure AI?
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Advanced AI technology that makes cybersecurity simple and effective
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:bg-white/15 transition-all duration-300 group"
              >
                <div className={`w-16 h-16 mb-6 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">{feature.title}</h3>
                <p className="text-gray-300 text-lg leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Simple. Smart. Secure.
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Three steps to complete cyber protection
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {[
              {
                step: '1',
                title: 'Deploy & Monitor',
                description: 'Set up smart honeypots that attract and monitor threats automatically',
                icon: Eye
              },
              {
                step: '2',
                title: 'AI Analysis',
                description: 'Advanced AI analyzes threats in real-time and learns attack patterns',
                icon: Brain
              },
              {
                step: '3',
                title: 'Auto Defense',
                description: 'System automatically responds to threats and strengthens defenses',
                icon: Shield
              }
            ].map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="text-center"
              >
                <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  {item.step}
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">{item.title}</h3>
                <p className="text-gray-300 text-lg leading-relaxed">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Cybersecurity Section */}
      <section className="py-24 bg-gradient-to-r from-red-600/10 to-orange-600/10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="w-16 h-16 mb-6 bg-gradient-to-r from-red-500 to-orange-500 rounded-2xl flex items-center justify-center">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-5xl font-bold text-white mb-6">
                Advanced <span className="text-red-400">Cybersecurity</span>
              </h2>
              <p className="text-xl text-gray-300 mb-6 leading-relaxed">
                Next-generation threat detection and response system that adapts to evolving cyber attacks in real-time.
              </p>
              <ul className="space-y-4 mb-8">
                {[
                  'Real-time threat monitoring and analysis',
                  'Adaptive honeypot technology',
                  'Automated incident response',
                  'Zero-day attack detection'
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center space-x-3 text-gray-300">
                    <CheckCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                    <span className="text-lg">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20"
            >
              <h3 className="text-2xl font-bold text-white mb-6">Security Metrics</h3>
              <div className="space-y-6">
                {[
                  { label: 'Threat Detection Rate', value: '99.8%', color: 'from-red-500 to-orange-500' },
                  { label: 'Response Time', value: '<50ms', color: 'from-orange-500 to-yellow-500' },
                  { label: 'False Positives', value: '0.02%', color: 'from-green-500 to-emerald-500' }
                ].map((metric, idx) => (
                  <div key={idx}>
                    <div className="flex justify-between mb-2">
                      <span className="text-gray-300">{metric.label}</span>
                      <span className="text-white font-bold">{metric.value}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className={`bg-gradient-to-r ${metric.color} h-2 rounded-full`} 
                           style={{width: idx === 0 ? '99%' : idx === 1 ? '95%' : '98%'}}></div>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* AI Section */}
      <section className="py-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="lg:order-2"
            >
              <div className="w-16 h-16 mb-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-5xl font-bold text-white mb-6">
                Intelligent <span className="text-purple-400">AI Engine</span>
              </h2>
              <p className="text-xl text-gray-300 mb-6 leading-relaxed">
                Machine learning algorithms that continuously learn from attack patterns to predict and prevent future threats.
              </p>
              <ul className="space-y-4 mb-8">
                {[
                  'Behavioral pattern recognition',
                  'Predictive threat modeling',
                  'Continuous learning algorithms',
                  'Anomaly detection system'
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center space-x-3 text-gray-300">
                    <CheckCircle className="w-5 h-5 text-purple-400 flex-shrink-0" />
                    <span className="text-lg">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="lg:order-1 bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20"
            >
              <h3 className="text-2xl font-bold text-white mb-6">AI Performance</h3>
              <div className="grid grid-cols-2 gap-6">
                {[
                  { label: 'Model Accuracy', value: '98.2%', icon: Target },
                  { label: 'Learning Speed', value: '24/7', icon: Zap },
                  { label: 'Data Processing', value: '1M+/sec', icon: Activity },
                  { label: 'Predictions', value: '99.5%', icon: TrendingUp }
                ].map((stat, idx) => (
                  <div key={idx} className="text-center">
                    <div className="w-16 h-16 mx-auto mb-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                      <stat.icon className="w-8 h-8 text-white" />
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                    <div className="text-gray-300 text-sm">{stat.label}</div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Blockchain Section */}
      <section className="py-24 bg-gradient-to-r from-green-600/10 to-blue-600/10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="w-16 h-16 mb-6 bg-gradient-to-r from-green-500 to-blue-500 rounded-2xl flex items-center justify-center">
                <Lock className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-5xl font-bold text-white mb-6">
                Secure <span className="text-green-400">Blockchain</span>
              </h2>
              <p className="text-xl text-gray-300 mb-6 leading-relaxed">
                Immutable logging and smart contract automation ensure tamper-proof evidence and automated response systems.
              </p>
              <ul className="space-y-4 mb-8">
                {[
                  'Immutable threat intelligence logs',
                  'Smart contract automation',
                  'Decentralized security network',
                  'Cryptographic proof of evidence'
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center space-x-3 text-gray-300">
                    <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                    <span className="text-lg">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20"
            >
              <h3 className="text-2xl font-bold text-white mb-6">Blockchain Stats</h3>
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                  <div>
                    <p className="text-white font-semibold">Total Blocks</p>
                    <p className="text-gray-300 text-sm">Immutable records</p>
                  </div>
                  <div className="text-2xl font-bold text-green-400">47,293</div>
                </div>
                <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                  <div>
                    <p className="text-white font-semibold">Smart Contracts</p>
                    <p className="text-gray-300 text-sm">Active automations</p>
                  </div>
                  <div className="text-2xl font-bold text-blue-400">156</div>
                </div>
                <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                  <div>
                    <p className="text-white font-semibold">Network Integrity</p>
                    <p className="text-gray-300 text-sm">Tamper-proof guarantee</p>
                  </div>
                  <div className="text-2xl font-bold text-green-400">100%</div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-blue-600/20 to-purple-600/20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-gray-300 mb-12">
              Experience the future of cybersecurity with BlockLure AI
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link href="/dashboard" className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-10 py-4 rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl inline-flex items-center space-x-3">
                <Shield className="w-6 h-6" />
                <span>Try Dashboard</span>
              </Link>
              <Link href="/about" className="bg-white/10 backdrop-blur-sm text-white px-10 py-4 rounded-xl font-semibold text-lg hover:bg-white/20 transition-all duration-300 border border-white/20 inline-flex items-center space-x-3">
                <CheckCircle className="w-5 h-5" />
                <span>Learn More</span>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
