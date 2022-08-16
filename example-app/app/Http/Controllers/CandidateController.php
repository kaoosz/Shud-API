<?php

namespace App\Http\Controllers;

use App\Models\Candidate;
use Illuminate\Http\Request;

class CandidateController extends Controller
{
    public function index()
    {
        //$can = Candidate::find(1)->simplePaginate(10);
        //$can = Candidate::paginate();
        $can = Candidate::query()
        ->search(request('search'))
        ->paginate()
        ->withQueryString();

        return view('candidates',compact('can'));
    }
}
