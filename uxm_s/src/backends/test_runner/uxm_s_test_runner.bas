#ifndef UXM_S_TEST_RUNNER_BAS
#define UXM_S_TEST_RUNNER_BAS

type UIRCompareResult
    testName As String
    interpreterCode As Long
    nativeCode As Long
    isEqual As Long
end type

function UXS_CompareInterpreterVsNative( _
    byval testName as String, _
    byval interpreterCode as Long, _
    byval nativeCode as Long _
) as UIRCompareResult
    dim r as UIRCompareResult
    r.testName = testName
    r.interpreterCode = interpreterCode
    r.nativeCode = nativeCode
    if interpreterCode = nativeCode then
        r.isEqual = -1
    else
        r.isEqual = 0
    end if
    return r
end function

function UXS_CompareResultJson(byref r as UIRCompareResult) as String
    dim s as String
    s = "{"
    s &= Chr(34) & "testName" & Chr(34) & ":" & Chr(34) & r.testName & Chr(34) & ","
    s &= Chr(34) & "interpreterCode" & Chr(34) & ":" & LTrim(Str(r.interpreterCode)) & ","
    s &= Chr(34) & "nativeCode" & Chr(34) & ":" & LTrim(Str(r.nativeCode)) & ","
    s &= Chr(34) & "isEqual" & Chr(34) & ":" & LTrim(Str(r.isEqual))
    s &= "}"
    return s
end function

#endif
