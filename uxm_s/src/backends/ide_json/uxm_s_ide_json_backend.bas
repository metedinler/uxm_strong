#ifndef UXM_S_IDE_JSON_BACKEND_BAS
#define UXM_S_IDE_JSON_BACKEND_BAS

' IDE icin zorunlu alanlar: tape, stack, data, flags, status
function UXS_BuildIdeStateJson( _
    byval tapeJson as String, _
    byval stackJson as String, _
    byval dataJson as String, _
    byval flagsValue as ULongInt, _
    byval statusValue as ULongInt _
) as String
    dim s as String
    s = "{"
    s &= Chr(34) & "tape" & Chr(34) & ":" & tapeJson & ","
    s &= Chr(34) & "stack" & Chr(34) & ":" & stackJson & ","
    s &= Chr(34) & "data" & Chr(34) & ":" & dataJson & ","
    s &= Chr(34) & "flags" & Chr(34) & ":" & LTrim(Str(flagsValue)) & ","
    s &= Chr(34) & "status" & Chr(34) & ":" & LTrim(Str(statusValue))
    s &= "}"
    return s
end function

function UXS_BuildOutputEnvelopeJson( _
    byval outputKind as String, _
    byval payloadJson as String, _
    byval successFlag as Long, _
    byval messageText as String _
) as String
    dim s as String
    s = "{"
    s &= Chr(34) & "kind" & Chr(34) & ":" & Chr(34) & outputKind & Chr(34) & ","
    s &= Chr(34) & "success" & Chr(34) & ":" & LTrim(Str(successFlag)) & ","
    s &= Chr(34) & "message" & Chr(34) & ":" & Chr(34) & messageText & Chr(34) & ","
    s &= Chr(34) & "payload" & Chr(34) & ":" & payloadJson
    s &= "}"
    return s
end function

#endif
