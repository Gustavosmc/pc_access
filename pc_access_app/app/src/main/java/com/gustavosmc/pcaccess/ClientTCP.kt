package com.gustavosmc.pcaccess

import android.util.Log
import java.io.DataInputStream
import java.io.DataOutputStream
import java.io.IOException
import java.io.Serializable
import java.net.InetSocketAddress
import java.net.Socket
import kotlin.properties.Delegates


class ClientTCP(ip: String = "", port: Int = 42424) : Thread(), Serializable{

    var serverIP: String by Delegates.notNull()
    var serverPort: Int by Delegates.notNull()
    private var wordsReceived: ArrayList<String>? = ArrayList()


    init {
        this.serverIP = ip
        this.serverPort = port
    }

    companion object {
        private const val TAG = "PCA_ClienteTCP"
        private const val TIME_MILIS_DELAY = 10L

        var isConnecting = false
        var isConnected = false
            @Synchronized
            set(value) {
                field = value
            }

        var socket: Socket? = null
        var input: DataInputStream? = null
        var output: DataOutputStream? = null
    }

    @Synchronized
    fun connect(): Boolean {
            Log.i(TAG, "Conectando $isConnected $isConnecting")
            if (isConnected || isConnecting) return false
            isConnecting = true
            try {
                Log.d(TAG, "$serverIP $serverPort")
                val socketAddress = InetSocketAddress(serverIP, serverPort)
                socket = Socket()
                socket!!.connect(socketAddress)
                input = DataInputStream(socket!!.getInputStream())
                output = DataOutputStream(socket!!.getOutputStream())
                isConnected = true
                this.start()
                Log.i(TAG, "Conectado $isConnected")
            } catch (e: Exception) {
                isConnecting = false
                Log.e(TAG, "Error ao conectar! " + e.message)
                e.printStackTrace()
            }
            isConnecting = false
            return isConnected
    }

    @Synchronized
    fun disconnect(): Boolean {
            Log.i(TAG, "Desconectando...")
            if (!isConnected) return false
            try {
                socket!!.close()
                input!!.close()
                output!!.close()
                isConnected = false
                Log.d(TAG, "Desconectado")
            } catch (e: IOException) {
                isConnected = false
                Log.e(TAG, """Erro ao desconectar! ${e.message}""")
                e.printStackTrace()
            }
            return true
    }

    @Synchronized
    @Throws(IOException::class)
    private fun send(msg: String) {
            output!!.write(msg.toByteArray(charset("UTF-8")))
            output!!.flush()
            Log.i(TAG, "Mensagem enviada!")
    }

    fun sendMessage(msg: String) {
        if (!isConnected) return
        Thread(Runnable {
            try {
                send(msg)
            } catch (e: IOException) {
                Log.e(TAG, """Erro ao enviar mensagem! ${e.message}""")
            }
        }).start()
    }

    @Synchronized
    fun recoverLast(): String {
        try {
            return if (wordsReceived!!.size > 0){
                val word = this.wordsReceived!![wordsReceived!!.lastIndex]
                this.wordsReceived!!.remove(word)
                word
            }else ""
        }catch (aiex : ArrayIndexOutOfBoundsException){
            Log.e(TAG, """Erro ao recuperar palavras! ${aiex.message}""")
        }
        return ""
    }

    override fun run(){
        Log.d(TAG, "executando")
        this.sendMessage(PCAConstants.PCA_CONNECT)
        while (isConnected) {
            val bytes = ByteArray(1024)
            val msg: String
            try {
                val size = input!!.read(bytes)
                if (size > -1) {
                    msg = String(bytes, 0, size, charset("UTF-8"))
                    wordsReceived!!.add(msg)
                    Log.d(TAG, msg)
                }
                Thread.sleep(TIME_MILIS_DELAY)
            } catch (e: Exception) {
                e.printStackTrace()
                Log.e(TAG, """Erro durante execução ${e.message}""")

            }

        }
    }



}