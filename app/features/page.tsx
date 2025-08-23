'use client'

import { motion } from 'framer-motion'
import { 
  Shield, 
  Brain, 
  Eye, 
  Zap, 
  Lock,
  BarChart3,
  AlertTriangle,
  CheckCircle
} from 'lucide-react'

const features = [
  {
    icon: Eye,
    title: 'Smart Honeypots',
    description: 'Intelligent decoy systems that adapt to attacker behavior',
    benefits: ['Real-time threat detection', 'Behavioral learning', 'Automatic adaptation', 'Zero false positives']
  },
  {
    icon: Brain,
    title: 'AI Threat Analysis',
    description: 'Advanced machine learning for instant threat classification',
    benefits: ['Pattern recognition', 'Predictive analysis', 'Continuous learning', '99.8% accuracy']
  },
  {
    icon: Shield,
    title: 'Automated Defense',
    description: 'Instant response system that blocks threats automatically',
    benefits: ['Sub-second response', 'Smart blocking', 'Adaptive rules', 'Zero downtime']
  },
  {
    icon: Lock,
    title: 'Secure Logging',
    description: 'Tamper-proof evidence collection and storage',
    benefits: ['Immutable records', 'Forensic ready', 'Compliance support', 'Audit trails']
  },
  {
    icon: BarChart3,
    title: 'Real-time Dashboard',
    description: 'Live monitoring and analytics for complete visibility',
    benefits: ['Live threat map', 'Performance metrics', 'Custom alerts', 'Easy reporting']
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Ultra-low latency detection and response system',
    benefits: ['<100ms response', 'High throughput', 'Scalable architecture', '99.99% uptime']
  }
]

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 pt-16">
      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h1 className="text-6xl md:text-7xl font-bold text-white mb-8">
              <span className="bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                Features
              </span>
            </h1>
            <p className="text-2xl text-gray-300 max-w-4xl mx-auto">
              Everything you need for complete cyber protection in one intelligent system
            </p>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:bg-white/15 transition-all duration-300"
              >
                <div className="w-16 h-16 mb-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center">
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">{feature.title}</h3>
                <p className="text-gray-300 mb-6 leading-relaxed">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.benefits.map((benefit, idx) => (
                    <li key={idx} className="flex items-center space-x-3 text-gray-300">
                      <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
                      <span>{benefit}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Performance Stats */}
      <section className="py-20 bg-white/5 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Proven Performance
            </h2>
            <p className="text-xl text-gray-300">
              Real numbers from real deployments
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { label: 'Threat Detection', value: '99.8%', icon: Shield },
              { label: 'Response Time', value: '<100ms', icon: Zap },
              { label: 'System Uptime', value: '99.99%', icon: CheckCircle },
              { label: 'False Positives', value: '0.02%', icon: AlertTriangle }
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <stat.icon className="w-10 h-10 text-white" />
                </div>
                <div className="text-4xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-gray-300 text-lg">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
