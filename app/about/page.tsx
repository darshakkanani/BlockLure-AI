'use client'

import { motion } from 'framer-motion'
import { 
  Shield, 
  Brain, 
  Users, 
  Award,
  Target,
  Zap
} from 'lucide-react'

const team = [
  {
    name: 'Dr. Sarah Chen',
    role: 'AI Research Lead',
    image: '/api/placeholder/200/200',
    bio: 'Leading expert in AI-driven cybersecurity with 15+ years of experience.'
  },
  {
    name: 'Prof. Michael Rodriguez',
    role: 'Security Architect',
    image: '/api/placeholder/200/200',
    bio: 'Cybersecurity pioneer and professor with deep expertise in threat detection.'
  },
  {
    name: 'Dr. Alex Kumar',
    role: 'Systems Engineer',
    image: '/api/placeholder/200/200',
    bio: 'Expert in honeypot technologies and network security systems.'
  }
]

export default function AboutPage() {
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
                About Us
              </span>
            </h1>
            <p className="text-2xl text-gray-300 max-w-4xl mx-auto">
              We're building the future of cybersecurity with AI-powered adaptive defense systems
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-white/5 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-5xl font-bold text-white mb-8">Our Mission</h2>
              <p className="text-xl text-gray-300 mb-6 leading-relaxed">
                To make cybersecurity simple, intelligent, and accessible for everyone. We believe that 
                advanced AI should protect organizations of all sizes from evolving cyber threats.
              </p>
              <p className="text-lg text-gray-400 leading-relaxed">
                BlockLure AI combines cutting-edge artificial intelligence with proven cybersecurity 
                principles to create adaptive defense systems that learn, evolve, and protect automatically.
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="grid grid-cols-2 gap-6"
            >
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20">
                <Shield className="w-12 h-12 text-blue-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Secure</h3>
                <p className="text-gray-300">Enterprise-grade security built from the ground up</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20">
                <Brain className="w-12 h-12 text-purple-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Intelligent</h3>
                <p className="text-gray-300">AI that learns and adapts to new threats automatically</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20">
                <Zap className="w-12 h-12 text-yellow-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Fast</h3>
                <p className="text-gray-300">Lightning-fast response times under 100ms</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20">
                <Target className="w-12 h-12 text-green-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Accurate</h3>
                <p className="text-gray-300">99.8% threat detection with minimal false positives</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Meet Our Team
            </h2>
            <p className="text-xl text-gray-300">
              World-class experts in AI, cybersecurity, and system architecture
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={member.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20 text-center"
              >
                <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <Users className="w-12 h-12 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">{member.name}</h3>
                <p className="text-blue-400 mb-4 font-semibold">{member.role}</p>
                <p className="text-gray-300 leading-relaxed">{member.bio}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-white/5 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Our Values
            </h2>
            <p className="text-xl text-gray-300">
              The principles that guide everything we do
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              {
                title: 'Innovation First',
                description: 'We push the boundaries of what\'s possible in cybersecurity, constantly exploring new ways to protect against evolving threats.',
                icon: Brain
              },
              {
                title: 'User-Centric Design',
                description: 'Complex security should be simple to use. We design intuitive interfaces that make advanced protection accessible to everyone.',
                icon: Users
              },
              {
                title: 'Transparency',
                description: 'We believe in open, honest communication about how our systems work and what they protect against.',
                icon: Shield
              },
              {
                title: 'Excellence',
                description: 'We strive for the highest standards in everything we build, from code quality to customer support.',
                icon: Award
              }
            ].map((value, index) => (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20"
              >
                <value.icon className="w-12 h-12 text-blue-400 mb-6" />
                <h3 className="text-2xl font-bold text-white mb-4">{value.title}</h3>
                <p className="text-gray-300 leading-relaxed">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-5xl font-bold text-white mb-6">
              Get In Touch
            </h2>
            <p className="text-xl text-gray-300 mb-12">
              Ready to learn more about BlockLure AI? We'd love to hear from you.
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <button className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-10 py-4 rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl">
                Contact Sales
              </button>
              <button className="bg-white/10 backdrop-blur-sm text-white px-10 py-4 rounded-xl font-semibold text-lg hover:bg-white/20 transition-all duration-300 border border-white/20">
                Schedule Demo
              </button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
