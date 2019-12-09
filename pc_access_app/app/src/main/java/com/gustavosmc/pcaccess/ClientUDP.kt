package com.gustavosmc.pcaccess

import android.util.Log
import java.io.IOException
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress

class ClientUDP(var host: String, var port: Int) {
    private val TAG = "PCA_ClientUDP"
    private val senderPort: Int = 0
    private val socket = DatagramSocket(senderPort)
    private val address = InetAddress.getByName(this.host)


    fun close(){
       if (! this.socket.isClosed){
           this.socket.disconnect()
           this.socket.channel?.disconnect()
           this.socket.close()
       }
    }

    fun send(data: ByteArray) {
        Thread(Runnable {
            try {
                val packet = DatagramPacket(data, data.size, this.address, port)
                    socket!!.send(packet)
            } catch (e: IOException) {
                Log.e(TAG, """Erro ao enviar mensagem! ${e.message}""")
            }
        }).start()
    }

}