package com.gustavosmc.pcaccess

import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.os.Bundle
import android.support.v4.app.ActivityCompat
import android.support.v4.content.ContextCompat
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.widget.TextView
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.content_main.*
import android.content.Intent
import android.icu.lang.UCharacter
import android.support.v7.widget.Toolbar
import android.view.*
import com.beust.klaxon.Klaxon
import com.gustavosmc.pc_access.R


class MainActivity : AppCompatActivity(), ExecutorInterface {

    private var speechToText: SpeechToText? = null
    private var firstTime = true
    private var scanCode = ScanCode(this)
    private lateinit var executor: Executor
    private lateinit var mouseSensor: MouseSensor

    /**
     * Campos e metodos de classe
     */
    companion object {
        private const val TAG = "PCA_MainActivity"
        private const val RECORD_REQUEST_CODE = 101
        private const val CAMERA_REQUEST_CODE = 102

        @Volatile
        var clientTCP: ClientTCP? = null
        @Volatile
        var clientUDP : ClientUDP? = null


        @SuppressLint("StaticFieldLeak")
        var subtitle: TextView? = null

        fun setSubtitle(text: String = "") {
            subtitle!!.text = text
        }
    }

    /**
     * Inicializa os components da view
     */
    private fun initComponents() {
        subtitle = tvOutput
    }

    /**
     * Inicializa os eventos das views
     */
    private fun initEvents() {


        tbConnect.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                doPermCamera()
                scanCode.scan()
            } else {
                stopSpeech()
                turn_off_mouse()
                disconnect()
            }
        }


        stSpeech.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked and ClientTCP.isConnected) {
                doPermAudio()
                startSpeech()
                ibSpeech.isClickable = false
                ibSpeech.alpha = 0.5f
            } else {
                stopSpeech()
                stSpeech.isChecked = false
                ibSpeech.isClickable = true
                ibSpeech.alpha = 1.0f
                if (!ClientTCP.isConnected) {
                    Toast.makeText(this, "Você tem que está conectado para ativar!", Toast.LENGTH_SHORT).show()
                }
            }
        }


        ibSpeech.setOnTouchListener { v, event ->
            if (ClientTCP.isConnected and !stSpeech.isChecked) {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        doPermAudio()
                        startSpeech()
                        stSpeech.alpha = 0.5f
                        stSpeech.isClickable = false
                    }
                    MotionEvent.ACTION_UP -> {
                        stopSpeech()
                        stSpeech.alpha = 1f
                        stSpeech.isClickable = true
                        stSpeech.isChecked = false
                    }
                }
            } else if (!ClientTCP?.isConnected && event?.action == MotionEvent.ACTION_DOWN ) {
                Toast.makeText(this@MainActivity, "Você tem que está conectado para ativar!", Toast.LENGTH_SHORT).show()
            }

            v?.onTouchEvent(event) ?: true
        }


        stMouse.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked && ClientTCP.isConnected) {
                clientTCP?.sendMessage("""${MouseSensor.FIXED_MOUSE} ${MouseSensor.FIXED_ON}""")
                ibMouse.isClickable = false
                ibMouse.alpha = 0.5f
            } else {
                clientTCP?.sendMessage("""${MouseSensor.FIXED_MOUSE} ${MouseSensor.FIXED_OFF}""")
                stMouse.isChecked = false
                ibMouse.isClickable = true
                ibMouse.alpha = 1.0f
                if (!ClientTCP.isConnected) {
                    Toast.makeText(this, "Você tem que está conectado para ligar o Mouse!", Toast.LENGTH_SHORT).show()
                }
            }
        }


        ibMouse.setOnTouchListener { v, event ->
            if (ClientTCP.isConnected && !stMouse.isChecked) {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        clientTCP?.sendMessage("""${MouseSensor.FIXED_MOUSE} ${MouseSensor.FIXED_ON}""")
                        stMouse.isClickable = false
                        stMouse.alpha = 0.5f
                    }
                    MotionEvent.ACTION_UP -> {
                        clientTCP?.sendMessage("""${MouseSensor.FIXED_MOUSE} ${MouseSensor.FIXED_OFF}""")
                        stMouse.isChecked = false
                        stMouse.isClickable = true
                        stMouse.alpha = 1.0f
                    }
                }
            } else if (!ClientTCP?.isConnected && event?.action == MotionEvent.ACTION_DOWN) {
                Toast.makeText(this@MainActivity, "Você tem que está conectado para ligar o Mouse!", Toast.LENGTH_SHORT).show()
            }
            v?.onTouchEvent(event) ?: true
        }


    } // End of initEvents


    private fun startSpeech() {
        speechToText!!.start()
    }

    private fun stopSpeech() {
        speechToText!!.stop()
    }

    private fun checkConnect() {
        tbConnect.isChecked = ClientTCP.isConnected
        if (!ClientTCP.isConnected) {
            stSpeech.isChecked = false
            stMouse.isChecked = false
        }
    }

    override fun turn_on_mouse(port: Int) {
        clientUDP = ClientUDP(clientTCP!!.serverIP, port)
        this.mouseSensor.startMouse()
    }

    override fun turn_off_mouse() {
        clientUDP?.close()
        this.mouseSensor.stopMouse()
    }

    override fun connect() {
        Thread(Runnable {
            clientTCP!!.connect()
            runOnUiThread {
                if (ClientTCP.isConnected) {
                    executor = Executor(this@MainActivity, clientTCP!!)
                    executor.start()
                    Toast.makeText(this@MainActivity, "Conectado", Toast.LENGTH_SHORT).show()
                } else
                    checkConnect()
            }
        }).start()
    }

    override fun disconnect() {
        Thread(Runnable {
            clientTCP!!.sendMessage(PCAConstants.PCA_DISCONNECT)
            Thread.sleep(1000)
            clientTCP!!.disconnect()
            runOnUiThread {
                checkConnect()
            }
        }).start()

    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        initComponents()
        initEvents()
        mouseSensor = MouseSensor(this)

        if (firstTime) {
            clientTCP = ClientTCP()
            speechToText = SpeechToText(clientTCP!!, this)
            firstTime = false
        }
    }


    override fun onDestroy() {
        super.onDestroy()
        try {
            stopSpeech()
            turn_off_mouse()
            disconnect()
        } catch (ex: Exception) {
            ex.printStackTrace()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == ScanCode.RESULT_READ_CODE) {
            Log.i(TAG, "onActivityResult qrcode " + data.toString())
            if (data != null) {
                scanCode.code = data.extras!!.getString(ScanCode.FLAG_SCAN_RESULT)
                try {
                    val connectionJO = Klaxon().parse<ConnectionJO>(scanCode.code)
                    val port = connectionJO!!.port
                    Log.e(TAG, port.toString())
                    for (ip in connectionJO.ips) {
                        if (!ClientTCP.isConnected) {
                            clientTCP!!.serverIP = ip
                            clientTCP!!.serverPort = port
                            Log.e(TAG, """Port: ${clientTCP!!.serverPort} IP: ${clientTCP!!.serverIP}""")
                            this.connect()
                        }
                    }
                } catch (e: Exception) {
                    checkConnect()
                    Log.e(TAG, e.toString())
                }

            } else
                checkConnect()
        }
    }

    /**
     * Realiza o pedido de permissão RECORD_AUDIO
     */
    private fun makeRequestAudio() {
        ActivityCompat.requestPermissions(this,
                arrayOf(android.Manifest.permission.RECORD_AUDIO),
                RECORD_REQUEST_CODE)
    }

    private fun doPermAudio() {
        val permission = ContextCompat.checkSelfPermission(this,
                android.Manifest.permission.RECORD_AUDIO)
        if (permission != PackageManager.PERMISSION_GRANTED) {
            Log.i(TAG, "Permission to record denied")
            makeRequestAudio()
        }
    }

    private fun makeRequestCamera() {
        ActivityCompat.requestPermissions(this,
                arrayOf(android.Manifest.permission.CAMERA),
                CAMERA_REQUEST_CODE)
    }

    private fun doPermCamera() {
        val permission = ContextCompat.checkSelfPermission(this,
                android.Manifest.permission.CAMERA)
        if (permission != PackageManager.PERMISSION_GRANTED) {
            Log.i(TAG, "Permission to camera denied")
            makeRequestCamera()
        }
    }


    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}
