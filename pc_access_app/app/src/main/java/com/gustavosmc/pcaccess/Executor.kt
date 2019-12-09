package com.gustavosmc.pcaccess

import android.util.Log

class Executor(private val executorSocket: ExecutorInterface,
               private val clientTCP: ClientTCP) : Thread() {
    private var running: Boolean = ClientTCP.isConnected
    private var lastWord: String = ""
    private val TAG = "PCA_Executor"


    override fun run() {
        super.run()
        while (running) {
            this.running = ClientTCP.isConnected
            lastWord = clientTCP.recoverLast()
            Log.d(TAG, lastWord)

            when(lastWord){
                PCAConstants.PCA_DISCONNECT -> {
                    Log.d(TAG, "desconectado")
                    executorSocket.disconnect()
                }
                PCAConstants.SERVER_MOUSE_ON -> {
                    Log.d(TAG, "mouse ligado")
                    executorSocket.turn_on_mouse(24242)
                }
                PCAConstants.SERVER_MOUSE_OFF -> {
                    Log.d(TAG, "mouse desligado")
                    executorSocket.turn_off_mouse()
                }
            }
            sleep(100)

        }
    }
}