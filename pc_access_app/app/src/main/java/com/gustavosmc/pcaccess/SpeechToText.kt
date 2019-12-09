package com.gustavosmc.pcaccess

import android.content.Context
import android.util.Log
import com.vikramezhil.droidspeech.DroidSpeech
import com.vikramezhil.droidspeech.OnDSListener
import com.vikramezhil.droidspeech.OnDSPermissionsListener

class SpeechToText(private val clientTCP: ClientTCP, context: Context) : OnDSListener,
        OnDSPermissionsListener {

    private var droidSpeech: DroidSpeech? = null

    init {
        droidSpeech = DroidSpeech(context, null)
        droidSpeech!!.setOnDroidSpeechListener(this)
        droidSpeech!!.setOfflineSpeechRecognition(false)

    }

    companion object {
        private const val TAG = "PCA_SpeechToText"
    }

    override fun onDroidSpeechRmsChanged(rmsChangedValue: Float) {
    }

    override fun onDroidSpeechSupportedLanguages(currentSpeechLanguage: String?,
                                                 upportedSpeechLanguages: MutableList<String>?) {

    }

    override fun onDroidSpeechAudioPermissionStatus(audioPermissionGiven: Boolean,
                                                    errorMsgIfAny: String?) {

    }

    override fun onDroidSpeechError(errorMsg: String?) {
    }

    override fun onDroidSpeechClosedByUser() {
    }

    override fun onDroidSpeechLiveResult(liveSpeechResult: String?) {
    }

    override fun onDroidSpeechFinalResult(finalSpeechResult: String?) {
        var text = finalSpeechResult
        clientTCP.sendMessage(text!!)
        MainActivity.setSubtitle(text!!)
        Log.d(TAG, text)
    }

    fun start(){
        droidSpeech!!.startDroidSpeechRecognition()
        Log.d(TAG, "start")
    }

    fun stop(){
        droidSpeech!!.closeDroidSpeechOperations()
    }



}