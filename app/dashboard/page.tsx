'use client'

import { motion } from 'framer-motion'
import { 
  Shield, 
  Activity, 
  AlertTriangle, 
  CheckCircle,
  TrendingUp,
  Users,
  Globe,
  Zap
} from 'lucide-react'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-2">
            Security Dashboard
          </h1>
          <p className="text-gray-300">
            Real-time threat monitoring and system status
          </p>
        </motion.div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Threats Blocked', value: '1,247', icon: Shield, color: 'from-green-500 to-emerald-500' },
            { label: 'Active Sessions', value: '23', icon: Users, color: 'from-blue-500 to-cyan-500' },
            { label: 'System Health', value: '98.5%', icon: Activity, color: 'from-purple-500 to-pink-500' },
            { label: 'Response Time', value: '87ms', icon: Zap, color: 'from-yellow-500 to-orange-500' }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-xl flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Threat Map */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="lg:col-span-2 bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20"
          >
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <Globe className="w-5 h-5 mr-2" />
              Live Threat Map
            </h3>
            <div className="h-80 bg-slate-800/50 rounded-xl flex items-center justify-center">
              <div className="text-center">
                <Globe className="w-16 h-16 text-blue-400 mx-auto mb-4" />
                <p className="text-gray-300">Interactive threat visualization</p>
                <p className="text-sm text-gray-400 mt-2">Monitoring global attack patterns</p>
              </div>
            </div>
          </motion.div>

          {/* Recent Alerts */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20"
          >
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2" />
              Recent Alerts
            </h3>
            <div className="space-y-4">
              {[
                { type: 'High', message: 'SSH brute force detected', time: '2 min ago', status: 'blocked' },
                { type: 'Medium', message: 'Suspicious port scan', time: '5 min ago', status: 'monitoring' },
                { type: 'Low', message: 'Failed login attempt', time: '8 min ago', status: 'logged' }
              ].map((alert, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-slate-800/50 rounded-lg">
                  <div className={`w-3 h-3 rounded-full ${
                    alert.type === 'High' ? 'bg-red-500' : 
                    alert.type === 'Medium' ? 'bg-yellow-500' : 'bg-green-500'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-white text-sm font-medium">{alert.message}</p>
                    <p className="text-gray-400 text-xs">{alert.time}</p>
                  </div>
                  <CheckCircle className="w-4 h-4 text-green-400" />
                </div>
              ))}
            </div>
          </motion.div>

          {/* AI Analysis */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20"
          >
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              AI Analysis
            </h3>
            <div className="space-y-4">
              <div className="p-4 bg-slate-800/50 rounded-lg">
                <p className="text-sm text-gray-300 mb-2">Threat Level</p>
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-green-500 to-yellow-500 h-2 rounded-full" style={{width: '35%'}}></div>
                  </div>
                  <span className="text-white text-sm font-medium">Low</span>
                </div>
              </div>
              <div className="p-4 bg-slate-800/50 rounded-lg">
                <p className="text-sm text-gray-300 mb-2">AI Confidence</p>
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full" style={{width: '92%'}}></div>
                  </div>
                  <span className="text-white text-sm font-medium">92%</span>
                </div>
              </div>
            </div>
          </motion.div>

          {/* System Status */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="lg:col-span-2 bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20"
          >
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2" />
              System Performance
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'CPU Usage', value: '45%', color: 'bg-blue-500' },
                { label: 'Memory', value: '67%', color: 'bg-green-500' },
                { label: 'Network', value: '23%', color: 'bg-purple-500' },
                { label: 'Storage', value: '34%', color: 'bg-yellow-500' }
              ].map((metric, index) => (
                <div key={index} className="text-center">
                  <div className="w-16 h-16 mx-auto mb-2 relative">
                    <div className="w-full h-full bg-gray-700 rounded-full"></div>
                    <div className={`absolute inset-0 ${metric.color} rounded-full`} 
                         style={{clipPath: `polygon(50% 50%, 50% 0%, ${50 + parseInt(metric.value)/2}% 0%, 50% 50%)`}}></div>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-white text-xs font-bold">{metric.value}</span>
                    </div>
                  </div>
                  <p className="text-gray-300 text-sm">{metric.label}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
