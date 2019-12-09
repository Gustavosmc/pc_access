package com.gustavosmc.pcaccess

import android.app.Activity
import android.content.Intent
import com.google.zxing.integration.android.IntentIntegrator
import com.gustavosmc.pc_access.R

class ScanCode() {
    private var activity: Activity? = null
    var code: String = ""

    companion object {
        const val RESULT_READ_CODE = 113
        const val FLAG_SCAN_RESULT = "SCAN_RESULT"
    }

    constructor(activity: Activity) : this() {
        this.activity = activity
    }

    fun scan() {
        if (activity == null) return
        val integrator = IntentIntegrator(this.activity)
        integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
        integrator.setPrompt(this.activity!!.getString(R.string.text_cam))
        integrator.setCameraId(0)
        integrator.setBeepEnabled(true)
        integrator.setBarcodeImageEnabled(true)
        integrator.setOrientationLocked(true)
        val intent: Intent = integrator.createScanIntent()
        this.activity!!.startActivityForResult(intent, RESULT_READ_CODE)
    }

}


