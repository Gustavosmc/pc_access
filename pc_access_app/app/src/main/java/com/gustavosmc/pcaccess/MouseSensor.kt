package com.gustavosmc.pcaccess

import android.content.Context
import android.hardware.*
import java.nio.charset.Charset
import java.util.*

class MouseSensor(context: Context) : SensorEventListener {
    private val TAG = "PCA_MouseSensor"
    private  var sensorManager: SensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    private lateinit var gyroscope: Sensor

    companion object {
        const val FIXED_MOUSE = "fk_mouse"
        const val FIXED_ON = "fk_on"
        const val FIXED_OFF = "fk_off"
    }

    init {
        this.sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)?.let {
            this.gyroscope = it
        }
    }

    fun startMouse(){
        this.sensorManager.registerListener(this, gyroscope, SensorManager.SENSOR_DELAY_GAME)
    }

    fun stopMouse(){
        this.sensorManager.unregisterListener(this)
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {

    }

    override fun onSensorChanged(event: SensorEvent?) {
        when (event?.sensor?.type) {
            Sensor.TYPE_GYROSCOPE -> {
                var x : Float = event.values[0]
                var y : Float = event.values[1]
                var z : Float = event.values[2]
                var msg_send = """%.9f,%.9f|""".format(Locale.ENGLISH, x, z)
                MainActivity.clientUDP!!.send(msg_send.toByteArray(Charset.defaultCharset()))



            }
        }
    }


}