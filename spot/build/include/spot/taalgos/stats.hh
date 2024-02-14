// -*- coding: utf-8 -*-
// Copyright (C) 2011, 2013, 2014, 2015 Laboratoire de Recherche et
// Développement de l'Epita (LRDE).
//
// This file is part of Spot, a model checking library.
//
// Spot is free software; you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// Spot is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
// or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
// License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#pragma once

#include <spot/ta/ta.hh>
#include <iosfwd>

namespace spot
{

  /// \addtogroup ta_misc
  /// @{

  struct SPOT_API ta_statistics
  {
    unsigned edges;
    unsigned states;
    unsigned acceptance_states;

    std::ostream& dump(std::ostream& out) const;
  };

  /// \brief Compute statistics for an automaton.
  SPOT_API ta_statistics stats_reachable(const const_ta_ptr& t);

  /// @}
}
